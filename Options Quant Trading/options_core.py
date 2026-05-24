from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable, Literal, Sequence


TRADING_DAYS = 252
CALENDAR_DAYS = 365

OptionRight = Literal["call", "put"]
VolUnit = Literal[
    "auto_annual",
    "decimal_annual",
    "percent_annual",
    "decimal_daily",
    "percent_daily",
]


@dataclass(frozen=True)
class Greeks:
    """Greeks are reported per contract before applying the contract multiplier."""

    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float


@dataclass(frozen=True)
class OptionLeg:
    """A signed option leg. Positive quantity is long; negative quantity is short."""

    right: OptionRight
    strike: float
    quantity: int = 1
    entry_price: float | None = None


@dataclass(frozen=True)
class StrategyMetrics:
    value: float
    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float


@dataclass(frozen=True)
class VolatilitySnapshot:
    current_iv: float
    forecast_rv: float
    iv_rank: float | None
    iv_percentile: float | None
    volatility_risk_premium: float
    expected_move_1sigma: float
    screen: str


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def validate_positive(name: str, value: float) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def normalize_implied_vol(
    value: float,
    unit: VolUnit = "auto_annual",
    trading_days: int = TRADING_DAYS,
) -> float:
    """
    Convert an implied-volatility observation to annual decimal volatility.

    The unit is deliberately explicit because data vendors differ:
    - decimal_annual: 0.25 means 25% annualized IV
    - percent_annual: 25 means 25% annualized IV
    - decimal_daily: 0.0157 means 1.57% daily IV, annualized by sqrt(252)
    - percent_daily: 1.57 means 1.57% daily IV, annualized by sqrt(252)
    - auto_annual: values above 3 are treated as annual percent, otherwise
      annual decimal. It never applies sqrt(252).
    """

    if value is None:
        raise ValueError("volatility value is required")

    vol = float(value)
    if not math.isfinite(vol) or vol < 0:
        raise ValueError("volatility must be finite and non-negative")

    unit = unit.lower()
    if unit == "auto_annual":
        return vol / 100.0 if vol > 3.0 else vol
    if unit == "decimal_annual":
        return vol
    if unit == "percent_annual":
        return vol / 100.0
    if unit == "decimal_daily":
        return vol * math.sqrt(trading_days)
    if unit == "percent_daily":
        return (vol / 100.0) * math.sqrt(trading_days)

    raise ValueError(f"unsupported volatility unit: {unit}")


def black_scholes_price(
    spot: float,
    strike: float,
    years: float,
    rate: float,
    vol: float,
    right: OptionRight = "call",
    dividend_yield: float = 0.0,
) -> float:
    spot = validate_positive("spot", spot)
    strike = validate_positive("strike", strike)
    years = max(float(years), 0.0)
    rate = float(rate)
    vol = max(float(vol), 0.0)
    dividend_yield = float(dividend_yield)
    right = right.lower()

    if right not in ("call", "put"):
        raise ValueError("right must be 'call' or 'put'")

    if years == 0.0:
        return max(spot - strike, 0.0) if right == "call" else max(strike - spot, 0.0)

    df_r = math.exp(-rate * years)
    df_q = math.exp(-dividend_yield * years)

    if vol == 0.0:
        forward_intrinsic = spot * df_q - strike * df_r
        return max(forward_intrinsic, 0.0) if right == "call" else max(-forward_intrinsic, 0.0)

    sqrt_t = math.sqrt(years)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * vol * vol) * years) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t

    if right == "call":
        return spot * df_q * norm_cdf(d1) - strike * df_r * norm_cdf(d2)
    return strike * df_r * norm_cdf(-d2) - spot * df_q * norm_cdf(-d1)


def option_greeks(
    spot: float,
    strike: float,
    years: float,
    rate: float,
    vol: float,
    right: OptionRight = "call",
    dividend_yield: float = 0.0,
) -> Greeks:
    spot = validate_positive("spot", spot)
    strike = validate_positive("strike", strike)
    years = max(float(years), 0.0)
    rate = float(rate)
    vol = max(float(vol), 0.0)
    dividend_yield = float(dividend_yield)
    right = right.lower()

    if right not in ("call", "put"):
        raise ValueError("right must be 'call' or 'put'")

    if years == 0.0 or vol == 0.0:
        if right == "call":
            delta = 1.0 if spot > strike else 0.0
        else:
            delta = -1.0 if spot < strike else 0.0
        return Greeks(delta=delta, gamma=0.0, vega=0.0, theta=0.0, rho=0.0)

    sqrt_t = math.sqrt(years)
    df_r = math.exp(-rate * years)
    df_q = math.exp(-dividend_yield * years)
    d1 = (math.log(spot / strike) + (rate - dividend_yield + 0.5 * vol * vol) * years) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    pdf = norm_pdf(d1)

    if right == "call":
        delta = df_q * norm_cdf(d1)
        theta_year = (
            -spot * df_q * pdf * vol / (2.0 * sqrt_t)
            - rate * strike * df_r * norm_cdf(d2)
            + dividend_yield * spot * df_q * norm_cdf(d1)
        )
        rho = strike * years * df_r * norm_cdf(d2) / 100.0
    else:
        delta = -df_q * norm_cdf(-d1)
        theta_year = (
            -spot * df_q * pdf * vol / (2.0 * sqrt_t)
            + rate * strike * df_r * norm_cdf(-d2)
            - dividend_yield * spot * df_q * norm_cdf(-d1)
        )
        rho = -strike * years * df_r * norm_cdf(-d2) / 100.0

    gamma = df_q * pdf / (spot * vol * sqrt_t)
    vega = spot * df_q * pdf * sqrt_t / 100.0
    theta = theta_year / CALENDAR_DAYS
    return Greeks(delta=delta, gamma=gamma, vega=vega, theta=theta, rho=rho)


def implied_volatility(
    option_price: float,
    spot: float,
    strike: float,
    years: float,
    rate: float,
    right: OptionRight = "call",
    dividend_yield: float = 0.0,
    lower: float = 1e-6,
    upper: float = 5.0,
    tolerance: float = 1e-7,
    max_iter: int = 120,
) -> float:
    option_price = validate_positive("option_price", option_price)

    low_price = black_scholes_price(spot, strike, years, rate, lower, right, dividend_yield)
    high_price = black_scholes_price(spot, strike, years, rate, upper, right, dividend_yield)
    if option_price < low_price - tolerance or option_price > high_price + tolerance:
        raise ValueError("option price is outside the supported implied-volatility range")

    lo, hi = lower, upper
    for _ in range(max_iter):
        mid = 0.5 * (lo + hi)
        price = black_scholes_price(spot, strike, years, rate, mid, right, dividend_yield)
        if abs(price - option_price) <= tolerance:
            return mid
        if price < option_price:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def strategy_metrics(
    legs: Sequence[OptionLeg],
    spot: float,
    days_to_expiry: float,
    rate: float,
    vol: float,
    dividend_yield: float = 0.0,
    contract_multiplier: int = 100,
) -> StrategyMetrics:
    years = max(float(days_to_expiry), 0.0) / CALENDAR_DAYS
    value = delta = gamma = vega = theta = rho = 0.0

    for leg in legs:
        qty = int(leg.quantity)
        px = black_scholes_price(spot, leg.strike, years, rate, vol, leg.right, dividend_yield)
        gr = option_greeks(spot, leg.strike, years, rate, vol, leg.right, dividend_yield)
        scale = qty * contract_multiplier
        value += px * scale
        delta += gr.delta * scale
        gamma += gr.gamma * scale
        vega += gr.vega * scale
        theta += gr.theta * scale
        rho += gr.rho * scale

    return StrategyMetrics(value=value, delta=delta, gamma=gamma, vega=vega, theta=theta, rho=rho)


def entry_value(
    legs: Sequence[OptionLeg],
    spot: float,
    days_to_expiry: float,
    rate: float,
    vol: float,
    dividend_yield: float = 0.0,
    contract_multiplier: int = 100,
) -> float:
    total = 0.0
    years = max(float(days_to_expiry), 0.0) / CALENDAR_DAYS
    for leg in legs:
        price = leg.entry_price
        if price is None:
            price = black_scholes_price(spot, leg.strike, years, rate, vol, leg.right, dividend_yield)
        total += int(leg.quantity) * float(price) * contract_multiplier
    return total


def strategy_value_under_scenario(
    legs: Sequence[OptionLeg],
    spot: float,
    remaining_days: float,
    rate: float,
    vol: float,
    dividend_yield: float = 0.0,
    contract_multiplier: int = 100,
) -> float:
    return strategy_metrics(
        legs=legs,
        spot=spot,
        days_to_expiry=remaining_days,
        rate=rate,
        vol=vol,
        dividend_yield=dividend_yield,
        contract_multiplier=contract_multiplier,
    ).value


def scenario_table(
    legs: Sequence[OptionLeg],
    spot: float,
    days_to_expiry: float,
    rate: float,
    vol: float,
    spot_moves_pct: Iterable[float],
    vol_moves_points: Iterable[float],
    days_elapsed: float = 0.0,
    dividend_yield: float = 0.0,
    contract_multiplier: int = 100,
) -> list[dict[str, float]]:
    initial = entry_value(legs, spot, days_to_expiry, rate, vol, dividend_yield, contract_multiplier)
    remaining_days = max(float(days_to_expiry) - float(days_elapsed), 0.0)
    rows: list[dict[str, float]] = []

    for spot_move in spot_moves_pct:
        scenario_spot = spot * (1.0 + float(spot_move) / 100.0)
        for vol_move in vol_moves_points:
            scenario_vol = max(vol + float(vol_move) / 100.0, 1e-6)
            value = strategy_value_under_scenario(
                legs,
                scenario_spot,
                remaining_days,
                rate,
                scenario_vol,
                dividend_yield,
                contract_multiplier,
            )
            rows.append(
                {
                    "spot_move_pct": float(spot_move),
                    "iv_move_points": float(vol_move),
                    "spot": scenario_spot,
                    "iv": scenario_vol,
                    "value": value,
                    "pnl": value - initial,
                }
            )
    return rows


def log_returns_from_prices(prices: Sequence[float]) -> list[float]:
    clean = [float(p) for p in prices if p is not None and math.isfinite(float(p)) and float(p) > 0]
    return [math.log(clean[i] / clean[i - 1]) for i in range(1, len(clean))]


def sample_std(values: Sequence[float]) -> float:
    vals = [float(v) for v in values if math.isfinite(float(v))]
    if len(vals) < 2:
        return 0.0
    mean = sum(vals) / len(vals)
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return math.sqrt(max(var, 0.0))


def realized_volatility_from_returns(
    returns: Sequence[float],
    trading_days: int = TRADING_DAYS,
) -> float:
    return sample_std(returns) * math.sqrt(trading_days)


def realized_volatility_from_prices(
    prices: Sequence[float],
    trading_days: int = TRADING_DAYS,
) -> float:
    return realized_volatility_from_returns(log_returns_from_prices(prices), trading_days)


def ewma_forecast_volatility(
    returns: Sequence[float],
    lambda_: float = 0.94,
    trading_days: int = TRADING_DAYS,
) -> float:
    vals = [float(r) for r in returns if math.isfinite(float(r))]
    if not vals:
        return 0.0
    lambda_ = min(max(float(lambda_), 0.0), 0.999)
    variance = vals[0] * vals[0]
    for ret in vals[1:]:
        variance = lambda_ * variance + (1.0 - lambda_) * ret * ret
    return math.sqrt(max(variance, 0.0)) * math.sqrt(trading_days)


def rank_and_percentile(current: float, history: Sequence[float]) -> tuple[float | None, float | None]:
    vals = [float(v) for v in history if math.isfinite(float(v))]
    if not vals:
        return None, None

    lo, hi = min(vals), max(vals)
    rank = None if hi == lo else (current - lo) / (hi - lo)
    percentile = sum(1 for v in vals if v <= current) / len(vals)
    if rank is not None:
        rank = min(max(rank, 0.0), 1.0)
    return rank, percentile


def volatility_snapshot(
    spot: float,
    current_iv: float,
    forecast_rv: float,
    days_to_expiry: float,
    iv_history: Sequence[float] | None = None,
) -> VolatilitySnapshot:
    iv_history = iv_history or []
    rank, percentile = rank_and_percentile(current_iv, iv_history)
    vrp = current_iv - forecast_rv
    expected_move = spot * current_iv * math.sqrt(max(days_to_expiry, 0.0) / CALENDAR_DAYS)

    if vrp > 0.05 and (percentile is None or percentile >= 0.6):
        screen = "short-vol candidate"
    elif vrp < -0.03 and (percentile is None or percentile <= 0.4):
        screen = "long-vol candidate"
    else:
        screen = "neutral / needs better edge"

    return VolatilitySnapshot(
        current_iv=current_iv,
        forecast_rv=forecast_rv,
        iv_rank=rank,
        iv_percentile=percentile,
        volatility_risk_premium=vrp,
        expected_move_1sigma=expected_move,
        screen=screen,
    )
