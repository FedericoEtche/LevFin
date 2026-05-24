"""Characteristic functions φ_T(u) = E[exp(i u ln S_T)] under the risk-neutral measure.

All functions return complex arrays with the same shape as `u`. They share signature
``phi(u, T, S0, r, q, params) -> complex array`` so any of them can plug into
``carr_madan.fft_call_prices``.

References
----------
- Heston: Little Heston Trap parametrization (Albrecher et al. 2007), numerically
  stable for long maturities. The original Heston (1993) form has a branch-cut
  discontinuity that breaks FFT for moderate T.
- Merton jump-diffusion: Merton (1976).
- Variance Gamma: Madan, Carr, Chang (1998).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class HestonParams:
    kappa: float   # mean-reversion speed
    theta: float   # long-run variance
    sigma: float   # vol-of-vol
    rho: float     # correlation between asset and variance
    v0: float      # initial variance


@dataclass(frozen=True)
class MertonParams:
    sigma: float       # diffusion vol (annualized)
    lam: float         # jump intensity (per year)
    mu_j: float        # mean of log-jump size
    sigma_j: float     # std of log-jump size


@dataclass(frozen=True)
class VGParams:
    sigma: float    # vol parameter
    nu: float       # variance rate of the gamma subordinator
    theta: float    # drift of the Brownian component


def bsm_cf(u, T, S0, r, q, sigma: float) -> np.ndarray:
    """Black-Scholes-Merton characteristic function. Useful as a baseline."""
    i = 1j
    u = np.asarray(u, dtype=complex)
    x0 = np.log(S0)
    return np.exp(i * u * (x0 + (r - q - 0.5 * sigma ** 2) * T) - 0.5 * sigma ** 2 * u ** 2 * T)


def heston_cf(u, T, S0, r, q, p: HestonParams) -> np.ndarray:
    """Heston CF — Little Heston Trap form.

    φ_T(u) = exp(C + D*v0 + i u ln S0)
    """
    i = 1j
    u = np.asarray(u, dtype=complex)
    x0 = np.log(S0)

    a = p.kappa * p.theta
    b = p.kappa - p.rho * p.sigma * i * u
    d = np.sqrt(b * b + p.sigma ** 2 * (i * u + u * u))
    g = (b - d) / (b + d)

    eDT = np.exp(-d * T)
    one_minus_g_eDT = 1.0 - g * eDT
    one_minus_g = 1.0 - g
    # numerical guards
    one_minus_g_eDT = np.where(np.abs(one_minus_g_eDT) < 1e-15, 1e-15, one_minus_g_eDT)
    one_minus_g = np.where(np.abs(one_minus_g) < 1e-15, 1e-15, one_minus_g)

    C = i * u * (r - q) * T + (a / p.sigma ** 2) * (
        (b - d) * T - 2.0 * np.log(one_minus_g_eDT / one_minus_g)
    )
    D = ((b - d) / p.sigma ** 2) * ((1.0 - eDT) / one_minus_g_eDT)
    return np.exp(C + D * p.v0 + i * u * x0)


def merton_cf(u, T, S0, r, q, p: MertonParams) -> np.ndarray:
    """Merton jump-diffusion CF.

    Asset dynamics:  dS/S = (r - q - λκ) dt + σ dW + (e^J - 1) dN,  J ~ N(μ_j, σ_j²)
    where κ = E[e^J] - 1 = exp(μ_j + σ_j²/2) - 1 (martingale correction).
    """
    i = 1j
    u = np.asarray(u, dtype=complex)
    x0 = np.log(S0)
    kappa_bar = np.exp(p.mu_j + 0.5 * p.sigma_j ** 2) - 1.0
    drift = r - q - 0.5 * p.sigma ** 2 - p.lam * kappa_bar

    diffusion_term = i * u * (x0 + drift * T) - 0.5 * p.sigma ** 2 * u ** 2 * T
    jump_cf = np.exp(i * u * p.mu_j - 0.5 * p.sigma_j ** 2 * u ** 2) - 1.0
    jump_term = p.lam * T * jump_cf
    return np.exp(diffusion_term + jump_term)


def variance_gamma_cf(u, T, S0, r, q, p: VGParams) -> np.ndarray:
    """Variance Gamma CF (Madan-Carr-Chang 1998).

    Includes the martingale correction ω = ln(1 - θν - σ²ν/2) / ν so that
    E[S_T] = S_0 e^{(r-q)T}.
    """
    i = 1j
    u = np.asarray(u, dtype=complex)
    x0 = np.log(S0)
    omega = np.log(1.0 - p.theta * p.nu - 0.5 * p.sigma ** 2 * p.nu) / p.nu
    drift = r - q + omega
    inner = 1.0 - i * u * p.theta * p.nu + 0.5 * p.sigma ** 2 * p.nu * u ** 2
    return np.exp(i * u * (x0 + drift * T)) * inner ** (-T / p.nu)
