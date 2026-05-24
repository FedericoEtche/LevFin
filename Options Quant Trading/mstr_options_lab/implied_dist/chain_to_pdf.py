"""Glue layer: option chain DataFrame → implied risk-neutral PDF for one expiry.

Pipeline
--------
1. Slice the chain to a single expiry, drop rows without usable mid/iv.
2. Build the OTM IV smile: for K > F use call IV, for K < F use put IV.
   (This avoids deep-ITM rows where bid-ask spread dominates and the
   put-call parity inversion noise destroys the smile.)
3. Fit Gatheral raw SVI to log-moneyness vs total variance.
4. Generate a dense K grid, BSM call prices from SVI(K), then ∂²C/∂K² → f(K).
5. Compute moments and percentiles for the summary panel.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import numpy as np
import pandas as pd

from ..config import CALENDAR_DAYS
from ..surface.svi import fit_svi_slice, svi_iv, SVIParams
from .breeden_litzenberger import risk_neutral_pdf_from_svi, risk_neutral_cdf


@dataclass
class ImpliedDistribution:
    expiry: date
    days_to_expiry: int
    spot: float
    forward: float
    rate: float
    dividend_yield: float
    svi: SVIParams
    K: np.ndarray            # strike grid
    pdf: np.ndarray          # f(K), integrates to 1
    cdf: np.ndarray          # F(K)
    atm_iv: float
    # moments / percentiles
    mean: float
    std: float
    skew: float
    kurt_excess: float
    p5: float
    p25: float
    p50: float
    p75: float
    p95: float
    n_strikes_used: int


def slice_to_otm_smile(
    chain: pd.DataFrame,
    expiry: date,
    forward: float,
    iv_col: str = "iv",
    strike_col: str = "strike",
    right_col: str = "right",
    min_iv: float = 0.05,
    max_iv: float = 5.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (log_moneyness, otm_iv) arrays for one expiry slice.

    For each strike we choose the OTM side (call for K > F, put for K < F).
    Rows with NaN/non-positive IV outside ``[min_iv, max_iv]`` are dropped.
    """
    sub = chain[chain["expiration"] == expiry].copy()
    if sub.empty:
        return np.array([]), np.array([])

    sub = sub[(sub[iv_col].notna()) & (sub[iv_col] > min_iv) & (sub[iv_col] < max_iv)]
    if sub.empty:
        return np.array([]), np.array([])

    sub["otm_right"] = np.where(sub[strike_col] >= forward, "call", "put")
    sub = sub[sub[right_col].astype(str).str.lower() == sub["otm_right"]]
    if sub.empty:
        # fallback: take any side that's available
        sub = chain[chain["expiration"] == expiry].copy()
        sub = sub[(sub[iv_col].notna()) & (sub[iv_col] > min_iv) & (sub[iv_col] < max_iv)]
        # dedupe by strike: average call+put IV
        sub = sub.groupby(strike_col, as_index=False)[iv_col].mean()

    sub = sub.sort_values(strike_col)
    K = sub[strike_col].to_numpy(dtype=float)
    iv = sub[iv_col].to_numpy(dtype=float)
    k_log = np.log(K / forward)
    return k_log, iv


def compute_implied_distribution(
    chain: pd.DataFrame,
    expiry: date,
    spot: float,
    rate: float,
    dividend_yield: float = 0.0,
    as_of: date | None = None,
    K_min_mult: float = 0.05,
    K_max_mult: float = 5.0,
    n_K: int = 1001,
) -> ImpliedDistribution:
    """Run the full pipeline for one expiry. Raises ValueError if too few strikes."""
    as_of = as_of or date.today()
    days = max((expiry - as_of).days, 1)
    T = days / float(CALENDAR_DAYS)
    F = spot * np.exp((rate - dividend_yield) * T)

    k_log, iv = slice_to_otm_smile(chain, expiry, forward=F)
    if k_log.size < 5:
        raise ValueError(
            f"Need at least 5 usable strikes to fit SVI; got {k_log.size} for {expiry}"
        )

    svi = fit_svi_slice(k_log, iv, T=T)
    K_grid, pdf = risk_neutral_pdf_from_svi(
        spot, svi, T, rate, dividend_yield,
        K_min=K_min_mult * F, K_max=K_max_mult * F, n_K=n_K,
    )
    cdf = risk_neutral_cdf(K_grid, pdf)

    # Moments
    dK = K_grid[1] - K_grid[0]
    mean = float(np.trapezoid(K_grid * pdf, K_grid))
    var = float(np.trapezoid((K_grid - mean) ** 2 * pdf, K_grid))
    std = float(np.sqrt(max(var, 0.0)))
    third = float(np.trapezoid((K_grid - mean) ** 3 * pdf, K_grid))
    fourth = float(np.trapezoid((K_grid - mean) ** 4 * pdf, K_grid))
    skew = third / std ** 3 if std > 0 else 0.0
    kurt_ex = fourth / std ** 4 - 3.0 if std > 0 else 0.0

    # Percentiles by inverting the CDF
    def pct(p: float) -> float:
        return float(np.interp(p, cdf, K_grid))

    # ATM IV from SVI
    atm_iv = float(svi_iv(np.array([0.0]), T, svi)[0])

    return ImpliedDistribution(
        expiry=expiry,
        days_to_expiry=days,
        spot=spot,
        forward=float(F),
        rate=rate,
        dividend_yield=dividend_yield,
        svi=svi,
        K=K_grid,
        pdf=pdf,
        cdf=cdf,
        atm_iv=atm_iv,
        mean=mean,
        std=std,
        skew=skew,
        kurt_excess=kurt_ex,
        p5=pct(0.05),
        p25=pct(0.25),
        p50=pct(0.50),
        p75=pct(0.75),
        p95=pct(0.95),
        n_strikes_used=int(k_log.size),
    )
