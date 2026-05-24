from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
import os
from pathlib import Path
import re
import sys
from typing import Any

import pandas as pd

from options_core import CALENDAR_DAYS, black_scholes_price  # still used by sample_mstr_chain


OPRA_DATASET = "OPRA.PILLAR"
DEFAULT_CACHE_DIR = Path("data_cache")
OCC_RE = re.compile(r"^(?P<root>.{6})(?P<expiry>\d{6})(?P<right>[CP])(?P<strike>\d{8})$")


@dataclass(frozen=True)
class DatabentoConfig:
    api_key: str | None = None
    dataset: str = OPRA_DATASET
    cache_dir: Path = DEFAULT_CACHE_DIR


def parent_symbol(underlying: str) -> str:
    return f"{underlying.strip().upper()}.OPT"


def parse_occ_symbol(raw_symbol: str) -> dict[str, Any]:
    """
    Parse OPRA/OCC 21-character option symbols such as:
    MSTR  260116C00500000
    """

    match = OCC_RE.match(str(raw_symbol))
    if not match:
        raise ValueError(f"not an OCC option symbol: {raw_symbol!r}")

    expiry_text = match.group("expiry")
    return {
        "underlying": match.group("root").strip(),
        "expiration": datetime.strptime(expiry_text, "%y%m%d").date(),
        "right": "call" if match.group("right") == "C" else "put",
        "strike": int(match.group("strike")) / 1000.0,
    }


def _ensure_databento_importable() -> None:
    vendor_dir = Path(__file__).resolve().parent / "databento-python-main"
    if vendor_dir.exists() and str(vendor_dir) not in sys.path:
        sys.path.insert(0, str(vendor_dir))


def historical_client(api_key: str | None = None):
    _ensure_databento_importable()
    import databento as db

    key = api_key or os.getenv("DATABENTO_API_KEY")
    return db.Historical(key=key) if key else db.Historical()


def _cache_path(config: DatabentoConfig, name: str) -> Path:
    config.cache_dir.mkdir(parents=True, exist_ok=True)
    return config.cache_dir / name


def _normalize_definition_frame(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    raw_col = "raw_symbol" if "raw_symbol" in df.columns else "symbol"
    rows: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        raw_symbol = row.get(raw_col)
        try:
            parsed = parse_occ_symbol(str(raw_symbol))
        except ValueError:
            continue
        rows.append(
            {
                "raw_symbol": str(raw_symbol),
                "underlying": parsed["underlying"],
                "expiration": parsed["expiration"],
                "right": parsed["right"],
                "strike": parsed["strike"],
                "instrument_id": row.get("instrument_id"),
            }
        )

    result = pd.DataFrame(rows)
    if result.empty:
        return result
    return result.drop_duplicates("raw_symbol").sort_values(["expiration", "strike", "right"]).reset_index(drop=True)


def fetch_option_definitions(
    underlying: str = "MSTR",
    start: str | date | None = None,
    config: DatabentoConfig | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    config = config or DatabentoConfig()
    query_date = start or date.today().isoformat()
    cache = _cache_path(config, f"{underlying.upper()}_definitions_{query_date}.parquet")
    if cache.exists():
        return pd.read_parquet(cache)

    client = historical_client(config.api_key)
    data = client.timeseries.get_range(
        dataset=config.dataset,
        schema="definition",
        stype_in="parent",
        symbols=[parent_symbol(underlying)],
        start=query_date,
        limit=limit,
    )
    df = _normalize_definition_frame(data.to_df())
    if not df.empty:
        df.to_parquet(cache, index=False)
    return df


def fetch_cmbp1_snapshot(
    symbols: list[str],
    start: str,
    end: str | None = None,
    config: DatabentoConfig | None = None,
    limit: int | None = None,
) -> pd.DataFrame:
    config = config or DatabentoConfig()
    if not symbols:
        return pd.DataFrame()

    client = historical_client(config.api_key)
    data = client.timeseries.get_range(
        dataset=config.dataset,
        schema="cmbp-1",
        stype_in="raw_symbol",
        symbols=symbols,
        start=start,
        end=end,
        limit=limit,
    )
    df = data.to_df()
    if df.empty:
        return df

    if "symbol" not in df.columns and "raw_symbol" in df.columns:
        df["symbol"] = df["raw_symbol"]
    return df.reset_index().sort_values("ts_recv").groupby("symbol", as_index=False).tail(1)


def estimate_request_cost(
    schema: str,
    symbols: list[str],
    start: str,
    end: str | None = None,
    underlying: str = "MSTR",
    stype_in: str = "raw_symbol",
    config: DatabentoConfig | None = None,
) -> float | None:
    config = config or DatabentoConfig()
    try:
        client = historical_client(config.api_key)
        return float(
            client.metadata.get_cost(
                dataset=config.dataset,
                schema=schema,
                symbols=symbols or [parent_symbol(underlying)],
                stype_in=stype_in,
                start=start,
                end=end,
            )
        )
    except Exception:
        return None


def enrich_chain_with_quotes(
    definitions: pd.DataFrame,
    quotes: pd.DataFrame,
    spot: float,
    rate: float,
    as_of: date | None = None,
    dividend_yield: float = 0.0,
) -> pd.DataFrame:
    """Merge quotes into definitions, then add IV and all 15 Greeks (vectorized).

    Greeks are stored as raw mathematical partial derivatives (per year, per unit
    vol). The workstation applies trader-unit scaling at display time via
    ``mstr_options_lab.greeks.trader_unit_scales()``.
    """
    if definitions.empty:
        return definitions

    as_of = as_of or date.today()
    chain = definitions.copy()
    if not quotes.empty:
        quote_cols = [c for c in ["symbol", "bid_px_00", "ask_px_00", "bid_sz_00", "ask_sz_00"] if c in quotes.columns]
        chain = chain.merge(quotes[quote_cols], left_on="raw_symbol", right_on="symbol", how="left")
    else:
        if "bid_px_00" not in chain.columns:
            chain["bid_px_00"] = pd.NA
        if "ask_px_00" not in chain.columns:
            chain["ask_px_00"] = pd.NA

    chain["mid"] = (pd.to_numeric(chain["bid_px_00"], errors="coerce") + pd.to_numeric(chain["ask_px_00"], errors="coerce")) / 2.0
    chain["days_to_expiry"] = chain["expiration"].apply(lambda exp: max((exp - as_of).days, 0))

    # Vectorized IV + Greeks (delta..ultima, 15 columns). Replaces the old per-row loop.
    from mstr_options_lab.greeks.chain import compute_chain_greeks
    chain = compute_chain_greeks(
        chain,
        spot=spot,
        rate=rate,
        dividend_yield=dividend_yield,
        calendar_days=CALENDAR_DAYS,
        inplace=True,
    )
    return chain


def sample_mstr_chain(
    as_of: date | None = None,
    spot: float = 178.0,
    sample_vol: float = 0.85,
    sample_rate: float = 0.045,
) -> pd.DataFrame:
    """Synthetic BSM-priced chain centered on ``spot``.

    Generates strikes from 0.6×spot to 1.4×spot in ~5% steps so that the chain
    actually looks like an ATM/near-ATM smile when the workstation enriches it.
    Keeps `sample_vol` constant (no real smile) — this is for offline UI dev.
    """
    as_of = as_of or date.today()
    expirations = [as_of + timedelta(days=30), as_of + timedelta(days=58)]
    # Strike grid centered on spot, ~17 strikes covering ±40%
    pct_grid = [0.60, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30, 1.40]
    # Round to nearest dollar for realistic OCC encoding
    strikes = sorted({round(spot * p) for p in pct_grid})
    rows: list[dict[str, Any]] = []
    for exp in expirations:
        exp_text = exp.strftime("%y%m%d")
        years = max((exp - as_of).days, 1) / CALENDAR_DAYS
        for strike in strikes:
            strike_text = f"{int(strike * 1000):08d}"
            for right, code in (("call", "C"), ("put", "P")):
                raw = f"{'MSTR':<6}{exp_text}{code}{strike_text}"
                fair = black_scholes_price(spot, strike, years, sample_rate, sample_vol, right)
                spread = max(0.05, fair * 0.02)
                rows.append(
                    {
                        "raw_symbol": raw,
                        "underlying": "MSTR",
                        "expiration": exp,
                        "right": right,
                        "strike": float(strike),
                        "instrument_id": None,
                        "bid_px_00": max(0.01, fair - spread / 2.0),
                        "ask_px_00": fair + spread / 2.0,
                    }
                )
    return pd.DataFrame(rows)
