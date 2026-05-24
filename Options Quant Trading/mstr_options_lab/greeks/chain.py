"""Vectorized Greek computation for an entire option chain DataFrame.

The data adapter (Databento / IBKR) hands us a chain with strike, days_to_expiry,
right, and a mid quote. We solve IV from mid, then compute every Greek (first,
second, third order) in one broadcast call.

Replaces the per-row ``iterrows()`` loop in the old ``enrich_chain_with_quotes``
— about 10× faster on a ~200-strike chain and adds 11 new Greek columns.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import CALENDAR_DAYS
from ..pricing.black_scholes import bs_implied_vol
from .analytical import bs_greeks


GREEK_COLUMNS_BASIC = ["delta", "gamma", "vega", "theta"]
GREEK_COLUMNS_HIGHER_ORDER = ["vanna", "charm", "vomma", "veta", "speed", "color", "zomma"]
GREEK_COLUMNS_FULL_TAIL = ["rho", "epsilon", "vera", "ultima"]
ALL_GREEK_COLUMNS = GREEK_COLUMNS_BASIC + GREEK_COLUMNS_HIGHER_ORDER + GREEK_COLUMNS_FULL_TAIL


def compute_chain_greeks(
    chain: pd.DataFrame,
    spot: float,
    rate: float,
    dividend_yield: float = 0.0,
    calendar_days: int = CALENDAR_DAYS,
    price_col: str = "mid",
    strike_col: str = "strike",
    days_col: str = "days_to_expiry",
    right_col: str = "right",
    iv_col: str = "iv",
    inplace: bool = False,
) -> pd.DataFrame:
    """Add IV + all 15 Greeks to ``chain`` as new columns. Returns the (modified) df.

    Greeks are stored as RAW mathematical partial derivatives:
        - theta is per year (multiply by 1/365 for $/day display)
        - vega is per unit vol (multiply by 0.01 for per-1%-vol)
        - rho/epsilon are per unit rate (multiply by 0.01 for per-1%-rate)
        - vanna, charm, vomma, veta, vera, zomma, color, ultima follow the same
          pattern: 1× per unit input. Workstation scales for display.

    Rows where the IV solver fails (price outside no-arb band, NaN inputs, etc.)
    have NaN in iv and all Greek columns — caller decides how to display.
    """
    if chain.empty:
        return chain if inplace else chain.copy()

    df = chain if inplace else chain.copy()
    strike = pd.to_numeric(df[strike_col], errors="coerce").to_numpy(dtype=float)
    days = pd.to_numeric(df[days_col], errors="coerce").to_numpy(dtype=float)
    price = pd.to_numeric(df[price_col], errors="coerce").to_numpy(dtype=float)
    right = df[right_col].astype(str).str.lower().to_numpy()

    years = np.where(days > 0, days / float(calendar_days), np.nan)

    # IV — only attempt where we have all inputs
    iv = bs_implied_vol(
        price,
        spot,
        strike,
        years,
        rate,
        right,
        dividend_yield,
    )
    df[iv_col] = iv

    # Greeks — vectorized; rows with NaN iv produce NaN greeks naturally
    g = bs_greeks(spot, strike, years, rate, iv, right, dividend_yield)
    df["delta"] = g.delta
    df["gamma"] = g.gamma
    df["vega"] = g.vega
    df["theta"] = g.theta
    df["rho"] = g.rho
    df["epsilon"] = g.epsilon
    df["vanna"] = g.vanna
    df["charm"] = g.charm
    df["vomma"] = g.vomma
    df["veta"] = g.veta
    df["vera"] = g.vera
    df["speed"] = g.speed
    df["zomma"] = g.zomma
    df["color"] = g.color
    df["ultima"] = g.ultima
    return df


def trader_unit_scales() -> dict[str, float]:
    """Map raw Greek column name → multiplier for trader-screen display.

    Multiply df[col] by this to get the conventional per-day / per-1pct values.
    """
    per_day = 1.0 / 365.0
    v1 = 0.01
    return {
        "delta": 1.0,
        "gamma": 1.0,
        "vega": v1,
        "theta": per_day,
        "rho": v1,
        "epsilon": v1,
        "vanna": v1,
        "charm": per_day,
        "vomma": v1 * v1,
        "veta": per_day * v1,
        "vera": v1 * v1,
        "speed": 1.0,
        "zomma": v1,
        "color": per_day,
        "ultima": v1 * v1 * v1,
    }
