"""GUI-free analytics and data orchestration for the desktop app."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
import math
import os
from typing import Iterable

import numpy as np
import pandas as pd

from databento_options import (
    DatabentoConfig,
    fetch_cmbp1_snapshot,
    fetch_option_definitions,
    sample_mstr_chain,
)
from mstr_options_lab.greeks.analytical import bs_greeks
from mstr_options_lab.implied_dist.breeden_litzenberger import (
    risk_neutral_cdf,
    risk_neutral_pdf_from_svi,
)
from mstr_options_lab.pricing.black_scholes import bs_implied_vol, bs_price
from mstr_options_lab.pricing.carr_madan import fft_price_one
from mstr_options_lab.pricing.characteristic_fns import (
    HestonParams,
    MertonParams,
    VGParams,
    bsm_cf,
    heston_cf,
    merton_cf,
    variance_gamma_cf,
)
from mstr_options_lab.surface.svi import SVIParams, fit_svi_slice, svi_iv
from options_core import CALENDAR_DAYS, OptionLeg, scenario_table, strategy_metrics


CHAIN_COLUMNS = [
    "raw_symbol",
    "expiration",
    "right",
    "strike",
    "bid_px_00",
    "ask_px_00",
    "mid",
    "iv",
    "fair_bsm",
    "edge_mid_minus_bsm",
    "delta",
    "gamma",
    "vega_1pct",
    "theta_day",
    "rho_1pct",
    "vanna_1pct",
    "charm_day",
    "vomma_1pct2",
    "volga_1pct2",
    "veta_day_1pct",
    "speed",
    "zomma_1pct",
    "color_day",
    "ultima_1pct3",
    "days_to_expiry",
]


@dataclass(frozen=True)
class ChainSummary:
    contracts: int
    expirations: int
    avg_iv: float | None
    nearest_atm: str | None
    spot: float


@dataclass(frozen=True)
class SmileFit:
    expiration: date
    years: float
    forward: float
    params: SVIParams
    observed: pd.DataFrame
    curve: pd.DataFrame


@dataclass(frozen=True)
class DistributionResult:
    expiration: date
    years: float
    grid: pd.DataFrame
    mean: float
    mode: float
    prob_below_spot: float
    prob_between_80_120_spot: float
    smile: SmileFit


def parse_date(value: str | date | datetime | pd.Timestamp | None, default: date | None = None) -> date:
    if value is None or value == "":
        return default or date.today()
    if isinstance(value, pd.Timestamp):
        return value.date()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return datetime.fromisoformat(str(value)).date()


def year_fraction(expiration: str | date | datetime | pd.Timestamp, as_of: date) -> float:
    exp = parse_date(expiration)
    return max((exp - as_of).days, 0) / CALENDAR_DAYS


def _coerce_numeric(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    out = frame.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def normalize_chain(
    chain: pd.DataFrame,
    spot: float,
    rate: float,
    dividend_yield: float,
    as_of: date,
) -> pd.DataFrame:
    """Add IV, BSM fair value, and higher-order Greeks to an option chain."""
    if chain.empty:
        return pd.DataFrame(columns=CHAIN_COLUMNS)

    out = chain.copy()
    if "raw_symbol" not in out.columns and "symbol" in out.columns:
        out["raw_symbol"] = out["symbol"]
    if "bid_px_00" not in out.columns:
        out["bid_px_00"] = np.nan
    if "ask_px_00" not in out.columns:
        out["ask_px_00"] = np.nan
    if "mid" not in out.columns:
        out["mid"] = np.nan

    out = _coerce_numeric(out, ["strike", "bid_px_00", "ask_px_00", "mid"])
    bid = out["bid_px_00"]
    ask = out["ask_px_00"]
    computed_mid = (bid + ask) / 2.0
    out["mid"] = out["mid"].where(out["mid"].notna(), computed_mid)
    out["mid"] = out["mid"].where(out["mid"] > 0, np.nan)

    out["expiration"] = out["expiration"].apply(parse_date)
    out["right"] = out["right"].astype(str).str.lower()
    out["days_to_expiry"] = out["expiration"].apply(lambda exp: max((exp - as_of).days, 0))
    years = out["days_to_expiry"].astype(float).to_numpy() / CALENDAR_DAYS

    strikes = out["strike"].astype(float).to_numpy()
    mids = out["mid"].astype(float).to_numpy()
    rights = out["right"].astype(str).to_numpy()

    iv = bs_implied_vol(
        option_price=mids,
        spot=float(spot),
        strike=strikes,
        years=years,
        rate=float(rate),
        right=rights,
        dividend_yield=float(dividend_yield),
    )
    out["iv"] = iv

    fair = bs_price(
        spot=float(spot),
        strike=strikes,
        years=years,
        rate=float(rate),
        vol=iv,
        right=rights,
        dividend_yield=float(dividend_yield),
    )
    out["fair_bsm"] = fair
    out["edge_mid_minus_bsm"] = out["mid"] - out["fair_bsm"]

    greeks = bs_greeks(
        spot=float(spot),
        strike=strikes,
        years=years,
        rate=float(rate),
        vol=iv,
        right=rights,
        dividend_yield=float(dividend_yield),
    )
    trader = greeks.to_trader_units()
    out["delta"] = trader["delta"]
    out["gamma"] = trader["gamma"]
    out["vega_1pct"] = trader["vega_per_1pct"]
    out["theta_day"] = trader["theta_per_day"]
    out["rho_1pct"] = trader["rho_per_1pct"]
    out["vanna_1pct"] = trader["vanna_per_1pct"]
    out["charm_day"] = trader["charm_per_day"]
    out["vomma_1pct2"] = trader["vomma_per_1pct2"]
    out["volga_1pct2"] = out["vomma_1pct2"]
    out["veta_day_1pct"] = trader["veta_per_day_per_1pct"]
    out["speed"] = trader["speed"]
    out["zomma_1pct"] = trader["zomma_per_1pct"]
    out["color_day"] = trader["color_per_day"]
    out["ultima_1pct3"] = trader["ultima_per_1pct3"]

    for col in CHAIN_COLUMNS:
        if col not in out.columns:
            out[col] = np.nan
    out = out[CHAIN_COLUMNS].sort_values(["expiration", "strike", "right"]).reset_index(drop=True)
    return out


def load_sample_chain(
    underlying: str,
    spot: float,
    rate: float,
    dividend_yield: float,
    as_of: date,
) -> pd.DataFrame:
    if underlying.strip().upper() != "MSTR":
        # The bundled sample generator is calibrated for MSTR. Keep the requested
        # label in the UI, but use MSTR-like synthetic contracts as a stable demo.
        underlying = "MSTR"
    return normalize_chain(sample_mstr_chain(as_of), spot, rate, dividend_yield, as_of)


def load_databento_chain(
    underlying: str,
    spot: float,
    rate: float,
    dividend_yield: float,
    as_of: date,
    definition_date: str,
    quote_start: str,
    quote_end: str,
    max_symbols: int,
) -> pd.DataFrame:
    if not os.getenv("DATABENTO_API_KEY"):
        raise RuntimeError("DATABENTO_API_KEY is not set. Set it in PowerShell before loading real data.")

    config = DatabentoConfig()
    definitions = fetch_option_definitions(
        underlying=underlying,
        start=definition_date,
        config=config,
    )
    if definitions.empty:
        return pd.DataFrame(columns=CHAIN_COLUMNS)

    near_chain = (
        definitions.assign(distance=(pd.to_numeric(definitions["strike"], errors="coerce") - float(spot)).abs())
        .sort_values(["expiration", "distance", "right"])
        .head(max(int(max_symbols), 1))
    )
    symbols = near_chain["raw_symbol"].dropna().astype(str).tolist()
    quotes = fetch_cmbp1_snapshot(
        symbols=symbols,
        start=quote_start,
        end=quote_end or None,
        config=config,
        limit=max(int(max_symbols), 1) * 100,
    )
    return normalize_chain(
        near_chain.drop(columns=["distance"], errors="ignore"),
        spot=spot,
        rate=rate,
        dividend_yield=dividend_yield,
        as_of=as_of,
    ) if quotes.empty else normalize_chain(
        near_chain.drop(columns=["distance"], errors="ignore").merge(
            quotes[[c for c in ["symbol", "bid_px_00", "ask_px_00", "bid_sz_00", "ask_sz_00"] if c in quotes.columns]],
            left_on="raw_symbol",
            right_on="symbol",
            how="left",
        ),
        spot=spot,
        rate=rate,
        dividend_yield=dividend_yield,
        as_of=as_of,
    )


def summarize_chain(chain: pd.DataFrame, spot: float) -> ChainSummary:
    if chain.empty:
        return ChainSummary(0, 0, None, None, spot)
    iv = pd.to_numeric(chain.get("iv"), errors="coerce").dropna()
    avg_iv = None if iv.empty else float(iv.mean())
    expirations = int(chain["expiration"].nunique()) if "expiration" in chain.columns else 0
    atm = None
    if "strike" in chain.columns and not chain["strike"].dropna().empty:
        row = chain.assign(distance=(chain["strike"] - spot).abs()).sort_values("distance").iloc[0]
        atm = f"{row['strike']:.0f} {str(row['right'])[0].upper()}"
    return ChainSummary(len(chain), expirations, avg_iv, atm, spot)


def available_expirations(chain: pd.DataFrame) -> list[date]:
    if chain.empty or "expiration" not in chain.columns:
        return []
    return sorted(parse_date(exp) for exp in chain["expiration"].dropna().unique())


def fit_smile(
    chain: pd.DataFrame,
    expiration: str | date,
    spot: float,
    rate: float,
    dividend_yield: float,
    as_of: date,
) -> SmileFit:
    exp = parse_date(expiration)
    years = year_fraction(exp, as_of)
    if years <= 0:
        raise ValueError("Selected expiration is not after the as-of date.")

    slice_df = chain[chain["expiration"].apply(parse_date) == exp].copy()
    slice_df = slice_df[np.isfinite(pd.to_numeric(slice_df["iv"], errors="coerce"))]
    slice_df = slice_df[(slice_df["iv"] > 0) & (slice_df["strike"] > 0)]
    if len(slice_df) < 5:
        raise ValueError("Need at least five valid IV points for an SVI smile fit.")

    forward = float(spot) * math.exp((float(rate) - float(dividend_yield)) * years)
    slice_df["log_moneyness"] = np.log(slice_df["strike"].astype(float) / forward)
    slice_df = slice_df.sort_values("log_moneyness")

    spread = (slice_df["ask_px_00"] - slice_df["bid_px_00"]).abs()
    weights = 1.0 / np.maximum(pd.to_numeric(spread, errors="coerce").fillna(1.0).to_numpy(), 0.05)
    params = fit_svi_slice(
        log_moneyness=slice_df["log_moneyness"].to_numpy(),
        market_iv=slice_df["iv"].to_numpy(),
        T=years,
        weights=weights,
    )

    k_min = float(slice_df["log_moneyness"].min())
    k_max = float(slice_df["log_moneyness"].max())
    pad = max(0.20, 0.10 * (k_max - k_min))
    k_grid = np.linspace(k_min - pad, k_max + pad, 300)
    iv_curve = svi_iv(k_grid, years, params)
    curve = pd.DataFrame(
        {
            "log_moneyness": k_grid,
            "strike": forward * np.exp(k_grid),
            "iv": iv_curve,
        }
    )
    return SmileFit(exp, years, forward, params, slice_df.reset_index(drop=True), curve)


def implied_distribution(
    chain: pd.DataFrame,
    expiration: str | date,
    spot: float,
    rate: float,
    dividend_yield: float,
    as_of: date,
) -> DistributionResult:
    smile = fit_smile(chain, expiration, spot, rate, dividend_yield, as_of)
    observed_strikes = smile.observed["strike"].astype(float)
    k_min = max(1.0, min(0.20 * smile.forward, 0.65 * float(observed_strikes.min())))
    k_max = max(1.50 * float(observed_strikes.max()), 2.50 * smile.forward)
    K, pdf = risk_neutral_pdf_from_svi(
        S0=float(spot),
        svi=smile.params,
        T=smile.years,
        r=float(rate),
        q=float(dividend_yield),
        K_min=k_min,
        K_max=k_max,
        n_K=1201,
    )
    cdf = risk_neutral_cdf(K, pdf)
    grid = pd.DataFrame({"strike": K, "pdf": pdf, "cdf": cdf})

    mean = float(np.trapezoid(K * pdf, K))
    mode = float(K[int(np.nanargmax(pdf))])
    prob_below_spot = float(np.interp(float(spot), K, cdf))
    lo = float(spot) * 0.8
    hi = float(spot) * 1.2
    prob_between = float(np.interp(hi, K, cdf) - np.interp(lo, K, cdf))
    return DistributionResult(smile.expiration, smile.years, grid, mean, mode, prob_below_spot, prob_between, smile)


def build_strategy_legs(strategy: str, strike1: float, strike2: float, contracts: int) -> list[OptionLeg]:
    contracts = int(contracts)
    if contracts <= 0:
        raise ValueError("Contracts must be positive.")
    low = min(float(strike1), float(strike2))
    high = max(float(strike1), float(strike2))
    name = strategy.strip().lower()
    if name == "long straddle":
        return [OptionLeg("call", float(strike1), contracts), OptionLeg("put", float(strike1), contracts)]
    if name == "short straddle":
        return [OptionLeg("call", float(strike1), -contracts), OptionLeg("put", float(strike1), -contracts)]
    if name == "long strangle":
        return [OptionLeg("put", low, contracts), OptionLeg("call", high, contracts)]
    if name == "short strangle":
        return [OptionLeg("put", low, -contracts), OptionLeg("call", high, -contracts)]
    if name == "long call vertical":
        return [OptionLeg("call", low, contracts), OptionLeg("call", high, -contracts)]
    if name == "short call vertical":
        return [OptionLeg("call", low, -contracts), OptionLeg("call", high, contracts)]
    if name == "long put vertical":
        return [OptionLeg("put", high, contracts), OptionLeg("put", low, -contracts)]
    if name == "short put vertical":
        return [OptionLeg("put", high, -contracts), OptionLeg("put", low, contracts)]
    raise ValueError(f"Unsupported strategy: {strategy}")


def price_strategy(
    strategy: str,
    spot: float,
    strike1: float,
    strike2: float,
    days_to_expiry: float,
    rate: float,
    vol: float,
    contracts: int,
) -> tuple[list[OptionLeg], object]:
    legs = build_strategy_legs(strategy, strike1, strike2, contracts)
    metrics = strategy_metrics(legs, spot, days_to_expiry, rate, vol)
    return legs, metrics


def strategy_grid(
    strategy: str,
    spot: float,
    strike1: float,
    strike2: float,
    days_to_expiry: float,
    rate: float,
    vol: float,
    contracts: int,
    spot_moves: Iterable[float],
    vol_moves: Iterable[float],
    days_elapsed: float,
) -> pd.DataFrame:
    legs = build_strategy_legs(strategy, strike1, strike2, contracts)
    rows = scenario_table(
        legs=legs,
        spot=spot,
        days_to_expiry=days_to_expiry,
        rate=rate,
        vol=vol,
        spot_moves_pct=list(spot_moves),
        vol_moves_points=list(vol_moves),
        days_elapsed=days_elapsed,
    )
    return pd.DataFrame(rows)


def model_price_table(
    spot: float,
    strike: float,
    days_to_expiry: float,
    rate: float,
    dividend_yield: float,
    vol: float,
    right: str,
) -> pd.DataFrame:
    T = max(float(days_to_expiry), 0.0) / CALENDAR_DAYS
    if T <= 0:
        raise ValueError("DTE must be positive for model comparison.")
    rows: list[dict[str, float | str]] = []
    bsm = float(bs_price(spot, strike, T, rate, vol, right, dividend_yield))
    rows.append({"model": "BSM closed form", "price": bsm})
    rows.append(
        {
            "model": "Carr-Madan FFT / BSM CF",
            "price": fft_price_one(bsm_cf, spot, strike, T, rate, dividend_yield, vol, right=right),
        }
    )

    heston_params = HestonParams(kappa=1.6, theta=vol * vol, sigma=0.55, rho=-0.55, v0=vol * vol)
    rows.append(
        {
            "model": "Carr-Madan FFT / Heston",
            "price": fft_price_one(heston_cf, spot, strike, T, rate, dividend_yield, heston_params, right=right),
        }
    )

    merton_params = MertonParams(sigma=max(vol * 0.75, 0.01), lam=0.65, mu_j=-0.03, sigma_j=0.18)
    rows.append(
        {
            "model": "Carr-Madan FFT / Merton jumps",
            "price": fft_price_one(merton_cf, spot, strike, T, rate, dividend_yield, merton_params, right=right),
        }
    )

    vg_params = VGParams(sigma=max(vol * 0.70, 0.01), nu=0.25, theta=-0.10)
    rows.append(
        {
            "model": "Carr-Madan FFT / Variance Gamma",
            "price": fft_price_one(variance_gamma_cf, spot, strike, T, rate, dividend_yield, vg_params, right=right),
        }
    )
    return pd.DataFrame(rows)


def parse_float_list(text: str) -> list[float]:
    values = [part.strip() for part in str(text).split(",") if part.strip()]
    if not values:
        raise ValueError("Expected a comma-separated list of numbers.")
    return [float(value) for value in values]
