"""Gatheral's "raw" SVI parameterization for a single maturity slice.

Total implied variance as a function of log-moneyness k = ln(K / F):

    w(k) = a + b · ( ρ · (k - m) + sqrt( (k - m)² + σ² ) )

Implied vol:  σ_BS(k) = sqrt( w(k) / T )

Parameter constraints for a well-posed slice (Roger Lee / Gatheral):
- b ≥ 0
- |ρ| < 1
- σ > 0
- a + b·σ·sqrt(1 - ρ²) ≥ 0      (ensures w ≥ 0 everywhere)
- b · (1 + |ρ|) ≤ 4 / T          (butterfly arb condition — large-strike wings)

Calendar-spread arb is between slices and must be enforced across maturities
(see surface/ssvi.py — not built yet).

Reference:
    Gatheral, J. (2004). "A parsimonious arbitrage-free implied volatility
    parameterization with application to the valuation of volatility derivatives."
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize


@dataclass
class SVIParams:
    a: float
    b: float
    rho: float
    m: float
    sigma: float


def svi_total_variance(k: np.ndarray, p: SVIParams) -> np.ndarray:
    k = np.asarray(k, dtype=float)
    return p.a + p.b * (p.rho * (k - p.m) + np.sqrt((k - p.m) ** 2 + p.sigma ** 2))


def svi_iv(k: np.ndarray, T: float, p: SVIParams) -> np.ndarray:
    w = np.maximum(svi_total_variance(k, p), 1e-12)
    return np.sqrt(w / T)


def _butterfly_arb_ok(p: SVIParams, T: float, k_grid: np.ndarray) -> bool:
    """Cheap check: g(k) = (1 - kw'/2w)² - w'²/4·(1/w + 1/4) + w''/2 ≥ 0 ?"""
    k = k_grid
    w = svi_total_variance(k, p)
    # Numerical first/second derivatives — sufficient for a sanity gate
    dk = k[1] - k[0]
    wp = np.gradient(w, dk)
    wpp = np.gradient(wp, dk)
    g = (1 - k * wp / (2 * np.maximum(w, 1e-12))) ** 2 - 0.25 * wp ** 2 * (
        1.0 / np.maximum(w, 1e-12) + 0.25
    ) + 0.5 * wpp
    return bool(np.all(g >= -1e-6))


def fit_svi_slice(
    log_moneyness: np.ndarray,
    market_iv: np.ndarray,
    T: float,
    weights: np.ndarray | None = None,
    enforce_arb: bool = True,
) -> SVIParams:
    """Least-squares fit to one expiry's smile.

    Parameters
    ----------
    log_moneyness : ndarray  k_i = ln(K_i / F)
    market_iv : ndarray      observed Black implied vols at those strikes
    T : float                year-fraction to expiry (matching the variance scaling)
    weights : optional       per-strike weights (typically 1/spread or 1/vega)
    enforce_arb : bool       if True, project to arb-bounds with a penalty term

    Returns
    -------
    SVIParams
    """
    k = np.asarray(log_moneyness, dtype=float)
    iv = np.asarray(market_iv, dtype=float)
    target_w = (iv ** 2) * T  # observed total variance
    if weights is None:
        weights = np.ones_like(k)
    else:
        weights = np.asarray(weights, dtype=float)

    # Seed: a near the lowest observed variance, b proportional to how steep the
    # wings rise; for an essentially flat smile, b → ~0 and a → constant.
    w_min = float(np.min(target_w))
    w_max = float(np.max(target_w))
    k_span = max(float(np.max(np.abs(k))), 1e-3)
    b0 = max((w_max - w_min) / k_span, 1e-4)
    x0 = np.array([max(w_min, 1e-6), b0, -0.3, 0.0, 0.1])

    def loss(x):
        a, b, rho, m, sig = x
        if b < 0 or abs(rho) >= 0.999 or sig <= 0:
            return 1e10
        if a + b * sig * np.sqrt(max(1 - rho ** 2, 0)) < 0:
            return 1e10
        if enforce_arb and b * (1 + abs(rho)) * T > 4:
            return 1e10
        w_pred = a + b * (rho * (k - m) + np.sqrt((k - m) ** 2 + sig ** 2))
        if np.any(w_pred < 0):
            return 1e10
        # Absolute residuals — robust to small target_w (relative is fragile)
        resid = w_pred - target_w
        return float(np.sum(weights * resid ** 2))

    bounds = [
        (-0.5, 1.0),      # a
        (1e-6, 5.0),      # b
        (-0.999, 0.999),  # rho
        (-2.0, 2.0),      # m
        (1e-4, 5.0),      # sigma
    ]
    res = minimize(loss, x0, method="L-BFGS-B", bounds=bounds)
    a, b, rho, m, sigma = res.x
    return SVIParams(a=float(a), b=float(b), rho=float(rho), m=float(m), sigma=float(sigma))
