"""Heston calibration to a market option chain.

Approach
--------
Joint calibration of (κ, θ, σ, ρ, v0) across all expiries simultaneously, with
multi-start L-BFGS-B. We minimize **vega-weighted price residuals**, which is
approximately equivalent to a sum-of-squared IV errors but avoids inverting the
Heston model price back to BSM IV at every loss eval (orders of magnitude
faster).

Filtering: OTM only (calls for K ≥ F, puts for K < F). Puts are converted to
call-equivalent via put-call parity so the loss can run on calls only.

Bounds (loosely consistent with Mikhailov & Nögel 2003, Lord 2008):
- κ  ∈ (0.1, 20)
- θ  ∈ (1e-4, 4.0)     long-run variance → annual vol up to 200%
- σ  ∈ (0.01, 5.0)     vol-of-vol
- ρ  ∈ (-0.99, 0.99)
- v0 ∈ (1e-4, 4.0)

Feller condition (2κθ ≥ σ²) is NOT hard-enforced — markets often violate it and
the Little Heston Trap CF is stable even when it does. A warning flag is
returned so caller can decide.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from typing import Sequence

import numpy as np
import pandas as pd
from scipy.optimize import minimize

from ..config import CALENDAR_DAYS
from .characteristic_fns import HestonParams, heston_cf
from .carr_madan import fft_prices_many_strikes


@dataclass
class _ExpiryBatch:
    T: float
    forward: float
    K: np.ndarray          # OTM strikes
    C_market: np.ndarray   # market call-equivalent prices (puts converted via parity)
    vega: np.ndarray       # market vega per option (for residual weighting)


@dataclass
class CalibrationResult:
    params: HestonParams
    rmse_iv_pts: float          # sqrt(mean of (price_err / vega)^2) in vol units
    rmse_iv_pct: float          # same, in vol points (×100)
    n_options: int
    n_expiries: int
    feller_ok: bool             # 2κθ ≥ σ² ?
    loss: float
    converged: bool
    n_starts: int

    def as_dict(self) -> dict:
        d = asdict(self)
        d["params"] = asdict(self.params)
        return d


def _estimate_atm_iv(chain: pd.DataFrame, spot: float, rate: float, dividend_yield: float) -> float:
    """Average ATM implied vol across expiries — used as a data-driven seed.

    Picks the strike closest to each expiry's forward, takes its IV (averaging
    call + put if both present), and returns the mean across expiries.
    Returns 0.5 if the chain has no usable IVs (graceful fallback).
    """
    df = chain.copy()
    df["T"] = pd.to_numeric(df.get("days_to_expiry"), errors="coerce") / float(CALENDAR_DAYS)
    df["forward"] = spot * np.exp((rate - dividend_yield) * df["T"])
    df = df[df["iv"].notna() & (df["iv"] > 0.05) & (df["iv"] < 5.0) & (df["T"] > 0)]
    if df.empty:
        return 0.5
    df["dist"] = (df["strike"] - df["forward"]).abs()
    # ATM-row per expiry — IV at the strike closest to forward
    atm_idx = df.groupby("T")["dist"].idxmin()
    return float(df.loc[atm_idx, "iv"].mean())


def _prepare_batches(
    chain: pd.DataFrame,
    spot: float,
    rate: float,
    dividend_yield: float,
    min_vega: float = 0.01,
) -> list[_ExpiryBatch]:
    df = chain.copy()
    df["T"] = pd.to_numeric(df.get("days_to_expiry"), errors="coerce") / float(CALENDAR_DAYS)
    df["forward"] = spot * np.exp((rate - dividend_yield) * df["T"])
    df["right_l"] = df["right"].astype(str).str.lower()

    # OTM only: calls when K ≥ F, puts when K < F
    df["is_otm"] = (
        ((df["right_l"] == "call") & (df["strike"] >= df["forward"])) |
        ((df["right_l"] == "put")  & (df["strike"] <  df["forward"]))
    )
    mask = (
        df["is_otm"]
        & df["mid"].notna() & (df["mid"] > 0)
        & df["iv"].notna() & (df["iv"] > 0.05) & (df["iv"] < 5.0)
        & df["vega"].notna() & (df["vega"] > min_vega)
        & (df["T"] > 0)
    )
    df = df[mask]

    batches: list[_ExpiryBatch] = []
    for T_val, group in df.groupby("T"):
        group = group.sort_values("strike")
        K = group["strike"].to_numpy(dtype=float)
        mids = group["mid"].to_numpy(dtype=float)
        rights = group["right_l"].to_numpy()
        F = float(group["forward"].iloc[0])
        T = float(T_val)
        DF_q = float(np.exp(-dividend_yield * T))
        DF_r = float(np.exp(-rate * T))
        # Convert OTM puts to call-equivalent via parity:  C = P + S·e^{-qT} - K·e^{-rT}
        call_market = np.where(rights == "call", mids, mids + spot * DF_q - K * DF_r)
        batches.append(
            _ExpiryBatch(
                T=T,
                forward=F,
                K=K,
                C_market=call_market,
                vega=group["vega"].to_numpy(dtype=float),
            )
        )
    return batches


def _loss_factory(
    spot: float,
    rate: float,
    dividend_yield: float,
    batches: Sequence[_ExpiryBatch],
    fft_N: int = 4096,
    fft_eta: float = 0.25,
    fft_alpha: float = 1.5,
):
    """Closure that returns the loss function for L-BFGS-B."""

    def loss(x: np.ndarray) -> float:
        kappa, theta, sigma, rho, v0 = x
        # The bounds passed to L-BFGS-B should keep us in-range; this is defensive
        if not (0 < kappa and 0 < theta and 0 < sigma and -1 < rho < 1 and 0 < v0):
            return 1e12
        params = HestonParams(kappa=kappa, theta=theta, sigma=sigma, rho=rho, v0=v0)
        total = 0.0
        for b in batches:
            try:
                C_model = fft_prices_many_strikes(
                    heston_cf, spot, b.K, b.T, rate, dividend_yield, params,
                    right="call", N=fft_N, eta=fft_eta, alpha=fft_alpha,
                )
            except Exception:
                return 1e12
            resid = (C_model - b.C_market) / np.maximum(b.vega, 1e-8)
            total += float(np.sum(resid * resid))
        return total

    return loss


def calibrate_heston(
    chain: pd.DataFrame,
    spot: float,
    rate: float,
    dividend_yield: float = 0.0,
    as_of: date | None = None,
    n_starts: int = 4,
    max_iter: int = 200,
    seed: int = 42,
    bounds: tuple | None = None,
) -> CalibrationResult:
    """Joint Heston calibration across all expiries in ``chain``.

    Returns a ``CalibrationResult`` with the best parameters and fit stats.
    Raises ``ValueError`` if the chain has too few usable options.
    """
    batches = _prepare_batches(chain, spot, rate, dividend_yield)
    n_options = sum(len(b.K) for b in batches)
    if n_options < 8 or len(batches) < 1:
        raise ValueError(
            f"Need at least 8 OTM options across at least 1 expiry; got {n_options} options across {len(batches)} expiries"
        )

    if bounds is None:
        bounds = [
            (0.1, 20.0),    # kappa
            (1e-4, 4.0),    # theta
            (0.01, 5.0),    # sigma
            (-0.99, 0.99),  # rho
            (1e-4, 4.0),    # v0
        ]

    loss = _loss_factory(spot, rate, dividend_yield, batches)

    # Data-driven deterministic seed: derive θ ≈ v0 ≈ ATM IV² from the chain itself.
    # This is essential for high-IV underlyings (MSTR ~85% IV) where a 60%-IV
    # default seed would put the optimizer in a much worse basin.
    atm_iv = _estimate_atm_iv(chain, spot, rate, dividend_yield)
    atm_var = max(atm_iv ** 2, 1e-3)
    sigma_volvol_seed = max(atm_iv, 0.3)  # floor so the smile term has room to flex
    deterministic_seed = (3.0, atm_var, sigma_volvol_seed, -0.5, atm_var)

    rng = np.random.default_rng(seed)
    seeds = [deterministic_seed]
    for _ in range(max(n_starts - 1, 0)):
        seeds.append((
            float(rng.uniform(*bounds[0])),
            float(rng.uniform(*bounds[1])),
            float(rng.uniform(*bounds[2])),
            float(rng.uniform(*bounds[3])),
            float(rng.uniform(*bounds[4])),
        ))

    best_res = None
    converged_any = False
    for x0 in seeds:
        try:
            res = minimize(
                loss, np.asarray(x0, dtype=float),
                method="L-BFGS-B", bounds=bounds,
                options={"maxiter": max_iter, "ftol": 1e-9, "gtol": 1e-7},
            )
        except Exception:
            continue
        if not np.isfinite(res.fun):
            continue
        if best_res is None or res.fun < best_res.fun:
            best_res = res
            converged_any = converged_any or bool(res.success)

    if best_res is None:
        raise RuntimeError("All Heston calibration starts failed")

    kappa, theta, sigma, rho, v0 = best_res.x
    params = HestonParams(kappa=float(kappa), theta=float(theta), sigma=float(sigma), rho=float(rho), v0=float(v0))
    rmse_iv = float(np.sqrt(best_res.fun / max(n_options, 1)))
    feller_ok = bool(2 * kappa * theta >= sigma ** 2)

    return CalibrationResult(
        params=params,
        rmse_iv_pts=rmse_iv,
        rmse_iv_pct=rmse_iv * 100.0,
        n_options=n_options,
        n_expiries=len(batches),
        feller_ok=feller_ok,
        loss=float(best_res.fun),
        converged=converged_any,
        n_starts=len(seeds),
    )
