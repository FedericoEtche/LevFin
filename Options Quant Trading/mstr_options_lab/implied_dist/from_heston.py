"""Risk-neutral PDF derived from a calibrated Heston model.

Uses the same Breeden-Litzenberger kernel as the SVI path so the two densities
can be plotted on the same axes for cross-validation:

    Heston params → FFT call curve on dense K grid → ∂²C/∂K² → f(K)

This is methodologically apples-to-apples with ``risk_neutral_pdf_from_svi``;
the only difference is the model used to interpolate the smile.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import savgol_filter

from ..pricing.carr_madan import fft_prices_many_strikes
from ..pricing.characteristic_fns import HestonParams, heston_cf
from .breeden_litzenberger import risk_neutral_pdf_from_calls, risk_neutral_cdf


def heston_pdf_for_expiry(
    S0: float,
    T: float,
    r: float,
    q: float,
    params: HestonParams,
    K_min: float | None = None,
    K_max: float | None = None,
    n_K: int = 1001,
    fft_N: int = 8192,
    fft_eta: float = 0.20,
    fft_alpha: float = 1.5,
    smooth_window: int = 31,
    smooth_poly: int = 3,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns (K_grid, pdf, cdf). PDF renormalized to integrate to 1.

    The B-L second difference amplifies FFT discretization noise in the deep
    OTM call wing — visible as ripple in the right tail of f(K). We apply
    a light Savitzky-Golay smoother (low-order, narrow window) to suppress
    this without distorting the bulk of the density. The smoother is
    optional — set ``smooth_window=0`` to disable.
    """
    F = S0 * np.exp((r - q) * T)
    K_min = K_min if K_min is not None else 0.05 * F
    K_max = K_max if K_max is not None else 5.0 * F
    K = np.linspace(K_min, K_max, n_K)
    C = fft_prices_many_strikes(
        heston_cf, S0, K, T, r, q, params,
        right="call", N=fft_N, eta=fft_eta, alpha=fft_alpha,
    )
    pdf = risk_neutral_pdf_from_calls(K, C, r=r, T=T)

    if smooth_window and smooth_window >= 5 and smooth_window < n_K:
        win = smooth_window if smooth_window % 2 == 1 else smooth_window + 1
        pdf = savgol_filter(pdf, window_length=win, polyorder=min(smooth_poly, win - 2))
        pdf = np.maximum(pdf, 0.0)

    area = float(np.trapezoid(pdf, K))
    if area > 0:
        pdf = pdf / area
    cdf = risk_neutral_cdf(K, pdf)
    return K, pdf, cdf
