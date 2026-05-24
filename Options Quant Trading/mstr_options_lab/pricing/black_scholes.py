"""Vectorized Black-Scholes-Merton pricing + implied volatility.

All inputs accept scalars or numpy arrays and broadcast.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import brentq
from scipy.stats import norm


def d1_d2(
    spot: ArrayLike,
    strike: ArrayLike,
    years: ArrayLike,
    rate: ArrayLike,
    vol: ArrayLike,
    dividend_yield: ArrayLike = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    spot = np.asarray(spot, dtype=float)
    strike = np.asarray(strike, dtype=float)
    years = np.asarray(years, dtype=float)
    rate = np.asarray(rate, dtype=float)
    vol = np.asarray(vol, dtype=float)
    dividend_yield = np.asarray(dividend_yield, dtype=float)

    sqrt_t = np.sqrt(years)
    # Guard against zero vol / zero T (caller handles intrinsic separately if needed)
    denom = np.where(vol * sqrt_t == 0, np.nan, vol * sqrt_t)
    d1 = (np.log(spot / strike) + (rate - dividend_yield + 0.5 * vol * vol) * years) / denom
    d2 = d1 - vol * sqrt_t
    return d1, d2


def bs_price(
    spot: ArrayLike,
    strike: ArrayLike,
    years: ArrayLike,
    rate: ArrayLike,
    vol: ArrayLike,
    right: str | ArrayLike = "call",
    dividend_yield: ArrayLike = 0.0,
) -> np.ndarray:
    """Black-Scholes-Merton price. `right` is "call"/"put" or an array of those."""
    spot = np.asarray(spot, dtype=float)
    strike = np.asarray(strike, dtype=float)
    years = np.asarray(years, dtype=float)
    rate = np.asarray(rate, dtype=float)
    vol = np.asarray(vol, dtype=float)
    dividend_yield = np.asarray(dividend_yield, dtype=float)

    is_call = _right_is_call(right, target_shape=np.broadcast(spot, strike, years, vol).shape)

    # Intrinsic handles T=0 and vol=0 corner cases cleanly
    fwd_disc = spot * np.exp(-dividend_yield * years)
    strike_disc = strike * np.exp(-rate * years)
    intrinsic_call = np.maximum(fwd_disc - strike_disc, 0.0)
    intrinsic_put = np.maximum(strike_disc - fwd_disc, 0.0)

    nontrivial = (years > 0) & (vol > 0)
    d1, d2 = d1_d2(spot, strike, years, rate, vol, dividend_yield)

    call = fwd_disc * norm.cdf(d1) - strike_disc * norm.cdf(d2)
    put = strike_disc * norm.cdf(-d2) - fwd_disc * norm.cdf(-d1)

    call = np.where(nontrivial, call, intrinsic_call)
    put = np.where(nontrivial, put, intrinsic_put)
    return np.where(is_call, call, put)


def _right_is_call(right, target_shape) -> np.ndarray:
    if isinstance(right, str):
        return np.full(target_shape, right.lower() == "call", dtype=bool)
    arr = np.asarray(right)
    if arr.dtype.kind in {"U", "S", "O"}:
        return np.char.lower(arr.astype(str)) == "call"
    return arr.astype(bool)


def bs_implied_vol(
    option_price: ArrayLike,
    spot: ArrayLike,
    strike: ArrayLike,
    years: ArrayLike,
    rate: ArrayLike,
    right: str | ArrayLike = "call",
    dividend_yield: ArrayLike = 0.0,
    lower: float = 1e-6,
    upper: float = 5.0,
    tol: float = 1e-10,
    max_iter: int = 40,
) -> np.ndarray:
    """Vectorized Halley IV solver with step-limited safeguards.

    Halley's method updates ``σ ← σ - 2·f·vega / (2·vega² - f·vomma)``. Cubic
    convergence in the interior; step magnitude is capped at ``0.5·σ`` per
    iteration to prevent overshoot near the boundary (deep ITM/OTM with
    vega ≈ 0). Where Halley's denominator is too small, falls through to
    Newton (single-derivative).

    Returns NaN for inputs that violate no-arb bounds or fail to converge.
    A Brent-based slow path is intentionally NOT included — convergence
    failures here propagate as NaN, and `compute_chain_greeks` skips them.
    """
    price = np.asarray(option_price, dtype=float)
    S = np.asarray(spot, dtype=float)
    K = np.asarray(strike, dtype=float)
    T = np.asarray(years, dtype=float)
    r = np.asarray(rate, dtype=float)
    q = np.asarray(dividend_yield, dtype=float)
    shape = np.broadcast(price, S, K, T, r, q).shape
    price, S, K, T, r, q = np.broadcast_arrays(price, S, K, T, r, q)
    is_call = _right_is_call(right, target_shape=shape)

    # Input validity
    valid = (
        np.isfinite(price) & np.isfinite(S) & np.isfinite(K) & np.isfinite(T)
        & (price > 0) & (T > 0) & (S > 0) & (K > 0)
    )
    DF_q = np.exp(-q * T)
    DF_r = np.exp(-r * T)
    intrinsic = np.where(
        is_call,
        np.maximum(S * DF_q - K * DF_r, 0.0),
        np.maximum(K * DF_r - S * DF_q, 0.0),
    )
    upper_bound = np.where(is_call, S * DF_q, K * DF_r)
    valid &= (price >= intrinsic - 1e-10) & (price <= upper_bound + 1e-10)

    # Robust initial guess: max of Brenner-Subrahmanyam-ish ATM proxy and a
    # moneyness-based floor. Conservative but always in-bounds.
    moneyness = np.where(K > 0, np.log(np.maximum(S, 1e-12) / np.maximum(K, 1e-12)), 0.0)
    sqrt_T0 = np.sqrt(np.maximum(T, 1e-12))
    bs_proxy = np.sqrt(np.maximum(2 * np.pi / np.maximum(T, 1e-8), 0.0)) * np.maximum(price - intrinsic, 1e-8) / np.maximum(S, 1e-8)
    sigma = np.clip(np.maximum(bs_proxy + 0.3 * np.abs(moneyness), 0.3), 0.05, 2.0)
    sigma = np.where(valid, sigma, np.nan)

    sqrt_2pi = np.sqrt(2 * np.pi)
    converged_mask = np.zeros_like(sigma, dtype=bool)
    for _ in range(max_iter):
        active = valid & ~converged_mask
        if not active.any():
            break
        sqrt_T = sqrt_T0
        sig_safe = np.where(np.isfinite(sigma), np.maximum(sigma, 1e-6), 0.3)
        d1 = (np.log(np.maximum(S, 1e-12) / np.maximum(K, 1e-12)) + (r - q + 0.5 * sig_safe ** 2) * T) / (sig_safe * sqrt_T)
        d2 = d1 - sig_safe * sqrt_T
        n_d1 = np.exp(-0.5 * d1 * d1) / sqrt_2pi

        call_p = S * DF_q * norm.cdf(d1) - K * DF_r * norm.cdf(d2)
        put_p = K * DF_r * norm.cdf(-d2) - S * DF_q * norm.cdf(-d1)
        model = np.where(is_call, call_p, put_p)

        vega = S * DF_q * n_d1 * sqrt_T
        vomma = vega * d1 * d2 / sig_safe

        f = model - price
        # Use absolute residual for convergence; tolerance is in price units
        newly_converged = np.abs(f) < tol
        converged_mask = converged_mask | (active & newly_converged)
        if (active & ~newly_converged).sum() == 0:
            break

        denom = 2.0 * vega * vega - f * vomma
        # Halley where stable, Newton where Halley's denom is unstable
        halley_step = np.where(np.abs(denom) > 1e-15, 2.0 * f * vega / denom, 0.0)
        newton_step = np.where(np.abs(vega) > 1e-15, f / vega, 0.0)
        step = np.where(np.abs(denom) > 1e-15, halley_step, newton_step)

        # Trust-region: cap step at 0.5·σ to prevent overshoot near boundaries
        max_step = 0.5 * sig_safe
        step = np.clip(step, -max_step, max_step)
        sigma = np.where(active, np.clip(sigma - step, lower, upper), sigma)

    out = np.where(converged_mask, sigma, np.nan)
    return out
