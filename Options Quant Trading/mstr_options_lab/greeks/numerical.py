"""Model-agnostic finite-difference Greeks.

Works on ANY pricer with signature ``price(S, K, T, r, q, **kwargs) -> float``,
which means Heston/FFT/VG/Merton Greeks come for free without re-deriving each.

For BSM, prefer ``analytical.bs_greeks`` — it's exact, no truncation error,
and orders of magnitude faster. Use these for non-BSM pricers.
"""

from __future__ import annotations

from typing import Callable

import numpy as np


def fd_greeks(
    pricer: Callable[..., float],
    S: float,
    K: float,
    T: float,
    r: float,
    q: float = 0.0,
    h_S: float | None = None,
    h_T: float | None = None,
    h_sigma: float = 1e-3,
    h_r: float = 1e-4,
    sigma_arg: str = "vol",
    **kwargs,
) -> dict:
    """Central-difference Greeks for any pricer.

    The pricer must accept (S, K, T, r, q, ...) and return a scalar option price.
    For models with a vol parameter (BSM, Heston-implied, etc.), pass its kwarg
    name as ``sigma_arg``. Models without a single σ parameter (e.g., raw Heston
    via FFT) can have their vega computed against a "shifted vol" reparam in caller.

    Returns a dict with as many Greeks as can be estimated.
    """
    h_S = h_S or max(1e-4 * S, 1e-2)
    h_T = h_T or 1.0 / 365.0  # one day

    def P(S_=S, T_=T, r_=r, q_=q, sigma_shift=0.0):
        kw = dict(kwargs)
        if sigma_arg in kw:
            kw[sigma_arg] = kw[sigma_arg] + sigma_shift
        return pricer(S_, K, T_, r_, q_, **kw)

    base = P()

    # Delta, Gamma, Speed
    pp = P(S_=S + h_S)
    pm = P(S_=S - h_S)
    delta = (pp - pm) / (2 * h_S)
    gamma = (pp - 2 * base + pm) / (h_S * h_S)
    ppp = P(S_=S + 2 * h_S)
    pmm = P(S_=S - 2 * h_S)
    speed = (ppp - 2 * pp + 2 * pm - pmm) / (2 * h_S ** 3)

    out = {"price": base, "delta": delta, "gamma": gamma, "speed": speed}

    # Theta (calendar-forward = -∂P/∂T)
    if T - h_T > 0:
        out["theta"] = -(P(T_=T + h_T) - P(T_=T - h_T)) / (2 * h_T)

    # Rho
    out["rho"] = (P(r_=r + h_r) - P(r_=r - h_r)) / (2 * h_r)

    # Vega, Vomma — only meaningful if pricer has a vol param
    if sigma_arg in kwargs:
        vp = P(sigma_shift=h_sigma)
        vm = P(sigma_shift=-h_sigma)
        vega = (vp - vm) / (2 * h_sigma)
        vomma = (vp - 2 * base + vm) / (h_sigma * h_sigma)
        out["vega"] = vega
        out["vomma"] = vomma

        # Vanna = ∂²P/∂S∂σ
        vpsp = P(S_=S + h_S, sigma_shift=h_sigma)
        vpsm = P(S_=S - h_S, sigma_shift=h_sigma)
        vmsp = P(S_=S + h_S, sigma_shift=-h_sigma)
        vmsm = P(S_=S - h_S, sigma_shift=-h_sigma)
        out["vanna"] = (vpsp - vpsm - vmsp + vmsm) / (4 * h_S * h_sigma)

        # Zomma = ∂²Γ/... wait, Zomma = ∂Γ/∂σ. Compute via mixed: (γ(σ+) - γ(σ-))/(2h_σ)
        # γ(σ) = (P(S+h)-2P+P(S-h))/h_S²
        def gamma_at(sig_shift=0.0):
            return (P(S_=S + h_S, sigma_shift=sig_shift)
                    - 2 * P(sigma_shift=sig_shift)
                    + P(S_=S - h_S, sigma_shift=sig_shift)) / (h_S * h_S)
        out["zomma"] = (gamma_at(h_sigma) - gamma_at(-h_sigma)) / (2 * h_sigma)

        # Ultima = ∂Vomma/∂σ = ∂³P/∂σ³  (3rd-derivative 5-point stencil)
        h3 = max(h_sigma, 1e-3)  # need bigger h for 3rd deriv to avoid noise
        out["ultima"] = (P(sigma_shift=2 * h3) - 2 * P(sigma_shift=h3)
                        + 2 * P(sigma_shift=-h3) - P(sigma_shift=-2 * h3)) / (2 * h3 ** 3)

        # Vera = ∂Vega/∂r = ∂²P/∂σ∂r
        out["vera"] = ((P(r_=r + h_r, sigma_shift=h_sigma) - P(r_=r - h_r, sigma_shift=h_sigma))
                       - (P(r_=r + h_r, sigma_shift=-h_sigma) - P(r_=r - h_r, sigma_shift=-h_sigma))) / (4 * h_r * h_sigma)

    # Time-derivative Greeks (calendar-forward: ∂/∂t = -∂/∂T)
    if T - h_T > 0:
        # Charm = ∂Δ/∂t  (calendar-forward)
        def delta_at(T_shift=0.0):
            return (P(T_=T + T_shift + h_S * 0, S_=S + h_S) - P(T_=T + T_shift, S_=S - h_S)) / (2 * h_S)
        # Note: dT increment is in T, but calendar-forward = -∂/∂T
        delta_Tp = (P(T_=T + h_T, S_=S + h_S) - P(T_=T + h_T, S_=S - h_S)) / (2 * h_S)
        delta_Tm = (P(T_=T - h_T, S_=S + h_S) - P(T_=T - h_T, S_=S - h_S)) / (2 * h_S)
        out["charm"] = -(delta_Tp - delta_Tm) / (2 * h_T)

        # Color = ∂Γ/∂t  (calendar-forward)
        def gamma_at_T(T_val):
            return (P(T_=T_val, S_=S + h_S) - 2 * P(T_=T_val) + P(T_=T_val, S_=S - h_S)) / (h_S * h_S)
        out["color"] = -(gamma_at_T(T + h_T) - gamma_at_T(T - h_T)) / (2 * h_T)

        # Veta = ∂Vega/∂t  (calendar-forward)
        if sigma_arg in kwargs:
            def vega_at_T(T_val):
                return (P(T_=T_val, sigma_shift=h_sigma) - P(T_=T_val, sigma_shift=-h_sigma)) / (2 * h_sigma)
            out["veta"] = -(vega_at_T(T + h_T) - vega_at_T(T - h_T)) / (2 * h_T)

    # Epsilon = ∂P/∂q
    out["epsilon"] = (P(q_=q + h_r) - P(q_=q - h_r)) / (2 * h_r)

    return out
