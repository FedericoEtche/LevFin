"""Carr-Madan FFT pricer.

Generic over any characteristic function ``phi(u, T, S0, r, q, params) -> complex``.
Returns calls; puts via put-call parity.

References
----------
Carr, P. & Madan, D. (1999). "Option Valuation Using the Fast Fourier Transform."
Journal of Computational Finance, 2(4), 61-73.

Conventions
-----------
- α is the damping factor that makes ψ(v) = e^{-rT} φ(v-i(α+1)) / [(α+iv)(α+iv+1)]
  square-integrable. α=1.5 is typical for equities; some models prefer α=0.75.
- Grid relation: Δv · Δk = 2π / N (uncertainty principle).
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def _simpson_weights(N: int) -> np.ndarray:
    if N % 2 != 0:
        raise ValueError("N must be even for Simpson weights")
    w = np.ones(N)
    w[1 : N - 1 : 2] = 4.0
    w[2 : N - 2 : 2] = 2.0
    return w


def fft_call_prices(
    phi: Callable,
    S0: float,
    T: float,
    r: float,
    q: float,
    params,
    N: int = 4096,
    eta: float = 0.25,
    alpha: float = 1.5,
):
    """Compute call prices on a log-strike grid via Carr-Madan FFT.

    Parameters
    ----------
    phi : callable
        Characteristic function ``phi(u, T, S0, r, q, params)``.
    N : int
        FFT length, power-of-two recommended, must be even.
    eta : float
        Frequency grid spacing Δv. Smaller → wider strike grid, less detail.
    alpha : float
        Damping factor (> 0).

    Returns
    -------
    K : ndarray  (N,) ascending strikes
    C : ndarray  (N,) call prices
    """
    n = np.arange(N)
    v = eta * n
    i = 1j

    phi_shift = phi(v - (alpha + 1) * i, T, S0, r, q, params)
    denom = alpha ** 2 + alpha - v ** 2 + i * (2 * alpha + 1) * v  # (α+iv)(α+iv+1)
    psi = np.exp(-r * T) * phi_shift / denom

    weights = _simpson_weights(N) * (eta / 3.0)
    lam = 2.0 * np.pi / (N * eta)         # log-strike step Δk
    b = 0.5 * N * lam                      # half-width in k
    x = psi * np.exp(1j * b * v) * weights

    F = np.real(np.fft.fft(x))
    k = -b + np.arange(N) * lam            # k = ln K
    K = np.exp(k)
    calls = np.exp(-alpha * k) / np.pi * F
    order = np.argsort(K)
    return K[order], np.maximum(calls[order], 0.0)


def fft_price_one(
    phi: Callable,
    S0: float,
    K: float,
    T: float,
    r: float,
    q: float,
    params,
    right: str = "call",
    N: int = 4096,
    eta: float = 0.25,
    alpha: float = 1.5,
) -> float:
    """Price a single strike via FFT + linear interpolation."""
    K_grid, C_grid = fft_call_prices(phi, S0, T, r, q, params, N=N, eta=eta, alpha=alpha)
    if K <= K_grid[0]:
        call = float(C_grid[0])
    elif K >= K_grid[-1]:
        call = float(C_grid[-1])
    else:
        idx = np.searchsorted(K_grid, K)
        x0, x1 = K_grid[idx - 1], K_grid[idx]
        y0, y1 = C_grid[idx - 1], C_grid[idx]
        call = float(y0 + (y1 - y0) * (K - x0) / (x1 - x0))
    if right.lower() == "call":
        return call
    # Put via put-call parity: P = C - S e^{-qT} + K e^{-rT}
    return call - S0 * np.exp(-q * T) + K * np.exp(-r * T)


def fft_prices_many_strikes(
    phi: Callable,
    S0: float,
    strikes: np.ndarray,
    T: float,
    r: float,
    q: float,
    params,
    right="call",
    N: int = 4096,
    eta: float = 0.25,
    alpha: float = 1.5,
) -> np.ndarray:
    """Vectorized: price an array of strikes against one expiry. Single FFT call."""
    K_grid, C_grid = fft_call_prices(phi, S0, T, r, q, params, N=N, eta=eta, alpha=alpha)
    calls = np.interp(strikes, K_grid, C_grid)
    is_call = (
        np.full(strikes.shape, str(right).lower() == "call", dtype=bool)
        if isinstance(right, str)
        else (np.char.lower(np.asarray(right).astype(str)) == "call")
    )
    puts = calls - S0 * np.exp(-q * T) + strikes * np.exp(-r * T)
    return np.where(is_call, calls, puts)
