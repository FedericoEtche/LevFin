"""Breeden-Litzenberger: recovering the risk-neutral density of S_T from option prices.

Theorem (Breeden & Litzenberger 1978):
    For European calls,  ∂²C(K,T) / ∂K² = e^{-rT} · f_{S_T}(K)
    where f is the risk-neutral PDF of the underlying at expiry T.

Practical issues with raw market quotes:
- Quotes are sparse in K and noisy (bid-ask + microstructure).
- A naive second difference of midpoint calls produces a very noisy "PDF" that
  often goes negative — i.e., not a valid density.

The right pipeline (this module):
1. Fit an arb-free smooth surface to the smile (we use Gatheral SVI per slice).
2. Generate a dense BSM call curve C(K) on a fine K grid from the fitted IV(K).
3. Apply ∂²C/∂K² to get f(K) — automatically arb-consistent since we fit a no-arb
   SVI.

Caller can also pass a pre-built call price function (e.g., from Heston FFT
after calibration) and get the density directly.
"""

from __future__ import annotations

from typing import Callable

import numpy as np

from ..pricing.black_scholes import bs_price
from ..surface.svi import SVIParams, svi_iv


def risk_neutral_pdf_from_calls(
    K_grid: np.ndarray,
    call_prices: np.ndarray,
    r: float,
    T: float,
) -> np.ndarray:
    """Density f(K) = e^{rT} · d²C/dK², second central difference.

    K_grid must be uniformly spaced. Returns array of the same length; the two
    endpoints are extrapolated by repeating their neighbours.
    """
    K = np.asarray(K_grid, dtype=float)
    C = np.asarray(call_prices, dtype=float)
    if K.size < 3:
        raise ValueError("Need at least 3 strikes")
    dK = K[1] - K[0]
    if not np.allclose(np.diff(K), dK, rtol=1e-6, atol=1e-9):
        raise ValueError("K_grid must be uniformly spaced for this estimator")
    pdf = np.empty_like(C)
    pdf[1:-1] = (C[2:] - 2.0 * C[1:-1] + C[:-2]) / (dK ** 2)
    pdf[0] = pdf[1]
    pdf[-1] = pdf[-2]
    pdf *= np.exp(r * T)
    # Clip tiny negative numerical noise to zero
    return np.maximum(pdf, 0.0)


def risk_neutral_pdf_from_svi(
    S0: float,
    svi: SVIParams,
    T: float,
    r: float,
    q: float = 0.0,
    K_min: float | None = None,
    K_max: float | None = None,
    n_K: int = 1001,
) -> tuple[np.ndarray, np.ndarray]:
    """Plug an SVI-fitted smile through BSM → finite-difference to obtain f(K).

    Returns (K_grid, density) where density integrates (approximately) to 1.
    """
    F = S0 * np.exp((r - q) * T)
    K_min = K_min if K_min is not None else 0.05 * F
    K_max = K_max if K_max is not None else 5.0 * F
    K = np.linspace(K_min, K_max, n_K)
    k_log = np.log(K / F)
    iv = svi_iv(k_log, T, svi)
    C = bs_price(S0, K, T, r, iv, "call", q)
    pdf = risk_neutral_pdf_from_calls(K, C, r=r, T=T)
    # renormalize to 1 for any numerical-trapezoid drift
    area = np.trapezoid(pdf, K)
    if area > 0:
        pdf = pdf / area
    return K, pdf


def risk_neutral_pdf(
    call_pricer: Callable[[np.ndarray], np.ndarray],
    K_grid: np.ndarray,
    r: float,
    T: float,
) -> np.ndarray:
    """Generic adapter: pass any call-price function K → C(K) and get f(K).

    Useful for Heston/FFT-calibrated models: define
        call_pricer = lambda K: fft_prices_many_strikes(heston_cf, S0, K, T, r, q, params)
    and the same numerical kernel produces the model's implied density.
    """
    C = call_pricer(np.asarray(K_grid))
    return risk_neutral_pdf_from_calls(K_grid, C, r=r, T=T)


def risk_neutral_cdf(K_grid: np.ndarray, pdf: np.ndarray) -> np.ndarray:
    """Cumulative density. Uses trapezoidal integration on the PDF."""
    K = np.asarray(K_grid, dtype=float)
    f = np.asarray(pdf, dtype=float)
    # cumulative trapezoid
    dK = np.diff(K)
    inc = 0.5 * (f[1:] + f[:-1]) * dK
    cdf = np.concatenate([[0.0], np.cumsum(inc)])
    if cdf[-1] > 0:
        cdf = cdf / cdf[-1]
    return cdf
