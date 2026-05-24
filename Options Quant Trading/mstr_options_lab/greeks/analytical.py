"""Closed-form Black-Scholes-Merton Greeks — first, second, and third order.

All Greeks are returned as RAW mathematical partial derivatives:
- Theta is per unit time (year), not per day. Multiply by 1/365 for daily display.
- Vega is per unit vol, not per 1%. Multiply by 0.01 for "vega per 1 vol point".
- Rho is per unit rate. Multiply by 0.01 for "rho per 1 bp" × 100.

A convenience method ``GreekSet.to_trader_units()`` applies the standard scalings.

References used (cross-checked):
- Wikipedia: "Greeks (finance)"
- Espen Haug, *The Complete Guide to Option Pricing Formulas* (2nd ed.)
- Wilmott, *Paul Wilmott on Quantitative Finance* (2nd ed.), Ch. 8

Sign conventions
----------------
- Theta and time-derivative Greeks (Charm, Veta, Color, DvegaDtime) are reported
  as ∂V/∂t where t is calendar-forward time (i.e., NEGATIVE of ∂V/∂T where T is
  time-to-expiry). This is the trader-standard "loss per day" convention.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import numpy as np
from numpy.typing import ArrayLike
from scipy.stats import norm

from ..pricing.black_scholes import d1_d2, _right_is_call


@dataclass
class GreekSet:
    # First-order
    delta: np.ndarray
    vega: np.ndarray         # ∂V/∂σ
    theta: np.ndarray        # ∂V/∂t (calendar-forward; per year)
    rho: np.ndarray          # ∂V/∂r
    epsilon: np.ndarray      # ∂V/∂q  (dividend rho / "psi")
    # Second-order
    gamma: np.ndarray
    vanna: np.ndarray        # ∂Δ/∂σ = ∂²V/∂S∂σ
    charm: np.ndarray        # ∂Δ/∂t (calendar-forward; per year)
    vomma: np.ndarray        # ∂Vega/∂σ = ∂²V/∂σ²  (also called "volga")
    veta: np.ndarray         # ∂Vega/∂t (calendar-forward; per year)
    vera: np.ndarray         # ∂²V/∂σ∂r
    # Third-order
    speed: np.ndarray        # ∂Γ/∂S = ∂³V/∂S³
    zomma: np.ndarray        # ∂Γ/∂σ
    color: np.ndarray        # ∂Γ/∂t (calendar-forward; per year)
    ultima: np.ndarray       # ∂Vomma/∂σ = ∂³V/∂σ³

    def to_trader_units(self) -> dict[str, Any]:
        """Apply the standard /day, /1%-vol, /1%-rate scalings used on trading screens."""
        per_day = 1.0 / 365.0
        v100 = 0.01
        r100 = 0.01
        return {
            "delta": self.delta,
            "gamma": self.gamma,
            "vega_per_1pct": self.vega * v100,
            "theta_per_day": self.theta * per_day,
            "rho_per_1pct": self.rho * r100,
            "epsilon_per_1pct": self.epsilon * r100,
            "vanna_per_1pct": self.vanna * v100,
            "charm_per_day": self.charm * per_day,
            "vomma_per_1pct2": self.vomma * v100 * v100,
            "veta_per_day_per_1pct": self.veta * per_day * v100,
            "vera_per_1pct2": self.vera * v100 * v100,
            "speed": self.speed,
            "zomma_per_1pct": self.zomma * v100,
            "color_per_day": self.color * per_day,
            "ultima_per_1pct3": self.ultima * v100 * v100 * v100,
        }

    def as_dict(self) -> dict[str, np.ndarray]:
        return asdict(self)


def bs_greeks(
    spot: ArrayLike,
    strike: ArrayLike,
    years: ArrayLike,
    rate: ArrayLike,
    vol: ArrayLike,
    right: str | ArrayLike = "call",
    dividend_yield: ArrayLike = 0.0,
) -> GreekSet:
    """Vectorized closed-form Greeks under BSM.

    Inputs broadcast. Returns a GreekSet whose arrays share the broadcast shape.
    """
    spot = np.asarray(spot, dtype=float)
    strike = np.asarray(strike, dtype=float)
    T = np.asarray(years, dtype=float)
    r = np.asarray(rate, dtype=float)
    sigma = np.asarray(vol, dtype=float)
    q = np.asarray(dividend_yield, dtype=float)

    shape = np.broadcast(spot, strike, T, r, sigma, q).shape
    is_call = _right_is_call(right, target_shape=shape)

    # core auxiliary quantities
    sqrt_T = np.sqrt(T)
    d1, d2 = d1_d2(spot, strike, T, r, sigma, q)
    n_d1 = norm.pdf(d1)
    DF_r = np.exp(-r * T)
    DF_q = np.exp(-q * T)

    # ===== First-order =====
    # Delta
    delta = np.where(is_call, DF_q * norm.cdf(d1), -DF_q * norm.cdf(-d1))

    # Vega — symmetric for call/put
    vega = spot * DF_q * n_d1 * sqrt_T

    # Theta (per year, calendar-forward convention: ∂V/∂t = -∂V/∂T)
    # ∂V/∂T_call = -S·e^{-qT}·n(d1)·σ/(2√T) + r·K·e^{-rT}·N(d2) - q·S·e^{-qT}·N(d1)
    # Trader-convention θ = -∂V/∂T
    theta_call = (
        -spot * DF_q * n_d1 * sigma / (2.0 * sqrt_T)
        - r * strike * DF_r * norm.cdf(d2)
        + q * spot * DF_q * norm.cdf(d1)
    )
    theta_put = (
        -spot * DF_q * n_d1 * sigma / (2.0 * sqrt_T)
        + r * strike * DF_r * norm.cdf(-d2)
        - q * spot * DF_q * norm.cdf(-d1)
    )
    theta = np.where(is_call, theta_call, theta_put)

    # Rho
    rho = np.where(
        is_call,
        strike * T * DF_r * norm.cdf(d2),
        -strike * T * DF_r * norm.cdf(-d2),
    )

    # Epsilon (dividend rho / "psi")
    epsilon = np.where(
        is_call,
        -spot * T * DF_q * norm.cdf(d1),
        spot * T * DF_q * norm.cdf(-d1),
    )

    # ===== Second-order =====
    # Gamma (symmetric)
    gamma = DF_q * n_d1 / (spot * sigma * sqrt_T)

    # Vanna = ∂Δ/∂σ = -e^{-qT}·n(d1)·(d2/σ)   (symmetric)
    vanna = -DF_q * n_d1 * d2 / sigma

    # Charm = ∂Δ/∂t (calendar-forward)
    # For a call:  Charm = q·e^{-qT}·N(d1) - e^{-qT}·n(d1)·[2(r-q)T - d2·σ·√T] / (2·T·σ·√T)
    # For a put:   Charm = -q·e^{-qT}·N(-d1) - e^{-qT}·n(d1)·[2(r-q)T - d2·σ·√T] / (2·T·σ·√T)
    charm_common = -DF_q * n_d1 * (2 * (r - q) * T - d2 * sigma * sqrt_T) / (2 * T * sigma * sqrt_T)
    charm = np.where(
        is_call,
        q * DF_q * norm.cdf(d1) + charm_common,
        -q * DF_q * norm.cdf(-d1) + charm_common,
    )

    # Vomma (Volga) = ∂Vega/∂σ = Vega · (d1·d2/σ)  (symmetric)
    vomma = vega * d1 * d2 / sigma

    # Veta = ∂Vega/∂t = -∂Vega/∂T (calendar-forward; symmetric).
    # Wikipedia and most refs present this as ∂Vega/∂T — we flip sign for the
    # calendar-forward convention used throughout this module.
    veta = spot * DF_q * n_d1 * sqrt_T * (
        q + (r - q) * d1 / (sigma * sqrt_T) - (1.0 + d1 * d2) / (2.0 * T)
    )

    # Vera = ∂²V/∂σ∂r = -K·T·e^{-rT}·n(d2)·d1/σ        (Wilmott)
    # symmetric in sign for call/put under this form
    vera = -strike * T * DF_r * norm.pdf(d2) * d1 / sigma

    # ===== Third-order =====
    # Speed = ∂Γ/∂S = -Γ/S · (d1/(σ√T) + 1)
    speed = -gamma / spot * (d1 / (sigma * sqrt_T) + 1.0)

    # Zomma = ∂Γ/∂σ = Γ · (d1·d2 - 1)/σ
    zomma = gamma * (d1 * d2 - 1.0) / sigma

    # Color = ∂Γ/∂t = -∂Γ/∂T (calendar-forward; symmetric).
    # Standard refs (Wikipedia, Wilmott) present this as ∂Γ/∂T — we flip sign
    # for the calendar-forward convention used throughout this module.
    color = DF_q * n_d1 / (2 * spot * T * sigma * sqrt_T) * (
        2 * q * T + 1.0 + (2 * (r - q) * T - d2 * sigma * sqrt_T) * d1 / (sigma * sqrt_T)
    )

    # Ultima = ∂Vomma/∂σ = ∂³V/∂σ³
    # Ultima = -Vega/σ² · [d1·d2·(1 - d1·d2) + d1² + d2²]
    ultima = -vega / (sigma ** 2) * (d1 * d2 * (1.0 - d1 * d2) + d1 ** 2 + d2 ** 2)

    # Suppress nonsensical values where T or σ → 0
    invalid = (T <= 0) | (sigma <= 0)
    # Use 0 for everything except delta/gamma which retain their limiting values
    def _z(x):
        return np.where(invalid, 0.0, x)

    # For delta at expiry under invalid path, fall back to forward intrinsic
    fwd_intrinsic_delta_call = np.where(spot > strike, 1.0, 0.0)
    fwd_intrinsic_delta_put = np.where(spot < strike, -1.0, 0.0)
    delta = np.where(
        invalid,
        np.where(is_call, fwd_intrinsic_delta_call, fwd_intrinsic_delta_put),
        delta,
    )

    return GreekSet(
        delta=np.asarray(delta),
        vega=_z(vega),
        theta=_z(theta),
        rho=_z(rho),
        epsilon=_z(epsilon),
        gamma=_z(gamma),
        vanna=_z(vanna),
        charm=_z(charm),
        vomma=_z(vomma),
        veta=_z(veta),
        vera=_z(vera),
        speed=_z(speed),
        zomma=_z(zomma),
        color=_z(color),
        ultima=_z(ultima),
    )
