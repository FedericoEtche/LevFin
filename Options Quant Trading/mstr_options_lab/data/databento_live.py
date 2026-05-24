"""Databento Live adapter — real-time equity spot and option chain.

Maps onto the subscription tier we confirmed live access for:
- ``EQUS.MINI`` for equity trades (US consolidated, sampled)
- ``OPRA.PILLAR`` for options (cmbp-1 NBBO + definition)

Schema matches the historical Databento adapter and IBKR adapter — same columns
(raw_symbol, expiration, right, strike, bid_px_00, ask_px_00, days_to_expiry,
underlying, instrument_id) so the workstation works unchanged regardless of source.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date
from typing import Optional

import numpy as np
import pandas as pd

from .. import config  # noqa: F401  — triggers .env.local load
from .databento import parent_symbol, parse_occ_symbol, OPRA_DATASET


DEFAULT_EQUITY_DATASET = "EQUS.MINI"
DEFAULT_OPTIONS_DATASET = OPRA_DATASET  # "OPRA.PILLAR"
FIXED_PRICE_SCALE = 1_000_000_000.0     # databento_dbn convention


@dataclass
class DatabentoLiveConfig:
    api_key: Optional[str] = None
    equity_dataset: str = DEFAULT_EQUITY_DATASET
    options_dataset: str = DEFAULT_OPTIONS_DATASET


class DatabentoLiveClient:
    """Live data adapter — spot via EQUS.MINI, options via OPRA.PILLAR."""

    def __init__(self, config: Optional[DatabentoLiveConfig] = None):
        self.config = config or DatabentoLiveConfig()
        self.api_key = self.config.api_key or os.getenv("DATABENTO_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "DATABENTO_API_KEY not set. Put it in .env.local at the project root."
            )

    # ---- Underlying spot ----
    def fetch_spot(self, symbol: str, timeout_seconds: float = 15.0) -> Optional[float]:
        """Return the next live trade price for ``symbol``. None if no trade within timeout.

        Uses the SDK callback API + block_for_close so a no-trade window doesn't
        hang the call — iteration-style consumption blocks until a record arrives.
        """
        import databento as db

        client = db.Live(key=self.api_key)
        found: dict[str, float] = {}

        def on_record(record) -> None:
            if "price" in found:
                return  # already got one
            if isinstance(record, db.TradeMsg):
                found["price"] = float(record.pretty_price)
                self._safe_stop(client)

        try:
            client.subscribe(
                dataset=self.config.equity_dataset,
                schema="trades",
                symbols=[symbol.upper()],
                stype_in="raw_symbol",
            )
            client.add_callback(on_record)
            client.start()
            client.block_for_close(timeout=timeout_seconds)
        finally:
            self._safe_stop(client)
        return found.get("price")

    # ---- Option chain ----
    def fetch_option_chain(
        self,
        symbol: str,
        spot_hint: float,
        *,
        max_expiries: int = 4,
        strike_window_pct: float = 0.40,
        listen_seconds: float = 10.0,
        as_of: Optional[date] = None,
    ) -> pd.DataFrame:
        """Pipeline: defs (Historical) → filter → live cmbp-1 (snapshot) → DataFrame."""
        import databento as db
        from databento_dbn import UNDEF_PRICE

        as_of = as_of or date.today()
        symbol = symbol.upper()

        # 1. Definitions via Historical — last complete trading day's snapshot.
        # The `definition` schema needs a UTC-midnight-aligned window; we use the
        # last fully-available calendar day so the query falls in a complete bucket.
        hist = db.Historical(key=self.api_key)
        rng = hist.metadata.get_dataset_range(dataset=self.config.options_dataset)
        end_date = pd.Timestamp(rng["end"]).date()
        start_date = end_date - pd.Timedelta(days=1)
        defs_data = hist.timeseries.get_range(
            dataset=self.config.options_dataset,
            schema="definition",
            symbols=[parent_symbol(symbol)],
            stype_in="parent",
            start=start_date.isoformat(),
            end=end_date.isoformat(),
        )
        defs_df = defs_data.to_df()
        if defs_df.empty:
            raise RuntimeError(f"No OPRA definitions found for {symbol}")

        # 2. Parse OCC + filter to N nearest expiries × strikes in window
        defs = _normalize_definitions(defs_df)
        if defs.empty:
            raise RuntimeError(f"Parsed 0 OCC symbols for {symbol}")
        keep_expiries = sorted(defs["expiration"].unique())[:max_expiries]
        defs = defs[defs["expiration"].isin(keep_expiries)]
        lo, hi = spot_hint * (1 - strike_window_pct), spot_hint * (1 + strike_window_pct)
        defs = defs[(defs["strike"] >= lo) & (defs["strike"] <= hi)].reset_index(drop=True)
        if defs.empty:
            raise RuntimeError(f"No strikes within {strike_window_pct:.0%} of spot {spot_hint}")

        symbols = defs["raw_symbol"].tolist()

        # 3. Live subscribe with snapshot for the filtered symbols. Callback API
        # avoids the iteration-style blocking when message rate is low.
        quotes: dict[int, dict[str, float]] = {}
        id_to_sym: dict[int, str] = {}
        live = db.Live(key=self.api_key)

        def on_record(record) -> None:
            if isinstance(record, db.SymbolMappingMsg):
                raw = getattr(record, "stype_in_symbol", None) or getattr(record, "raw_symbol", None)
                if raw:
                    id_to_sym[int(record.instrument_id)] = str(raw).strip()
                return
            if isinstance(record, db.CMBP1Msg):
                iid = int(record.instrument_id)
                levels = record.levels
                if not levels:
                    return
                lvl = levels[0]
                bid = float(lvl.bid_px) / FIXED_PRICE_SCALE if lvl.bid_px != UNDEF_PRICE else float("nan")
                ask = float(lvl.ask_px) / FIXED_PRICE_SCALE if lvl.ask_px != UNDEF_PRICE else float("nan")
                quotes[iid] = {"bid_px_00": bid, "ask_px_00": ask}

        try:
            # Note: OPRA.PILLAR live does NOT support snapshot=True for cmbp-1
            # (gateway error: "Snapshot subscription is currently not supported").
            # We listen for organic NBBO updates; liquid ATM strikes will quote
            # multiple times per second, deep OTM may have gaps within the window.
            live.subscribe(
                dataset=self.config.options_dataset,
                schema="cmbp-1",
                symbols=symbols,
                stype_in="raw_symbol",
            )
            live.add_callback(on_record)
            live.start()
            live.block_for_close(timeout=listen_seconds)
        finally:
            self._safe_stop(live)

        # 4. Merge defs + live quotes (key by raw_symbol via id_to_sym map)
        defs["bid_px_00"] = np.nan
        defs["ask_px_00"] = np.nan
        sym_to_quote: dict[str, dict[str, float]] = {}
        for iid, q in quotes.items():
            sym = id_to_sym.get(iid)
            if sym:
                sym_to_quote[sym] = q
        for i, row in defs.iterrows():
            q = sym_to_quote.get(row["raw_symbol"])
            if q is not None:
                defs.at[i, "bid_px_00"] = q["bid_px_00"]
                defs.at[i, "ask_px_00"] = q["ask_px_00"]

        defs["underlying"] = symbol
        defs["days_to_expiry"] = defs["expiration"].apply(lambda e: max((e - as_of).days, 0))
        return defs.sort_values(["expiration", "strike", "right"]).reset_index(drop=True)

    # ---- helpers ----
    @staticmethod
    def _safe_stop(client) -> None:
        try:
            client.stop()
        except Exception:
            pass


def _normalize_definitions(df: pd.DataFrame) -> pd.DataFrame:
    raw_col = "raw_symbol" if "raw_symbol" in df.columns else "symbol"
    rows = []
    for _, r in df.iterrows():
        try:
            parsed = parse_occ_symbol(str(r[raw_col]))
        except ValueError:
            continue
        rows.append({
            "raw_symbol": str(r[raw_col]),
            "instrument_id": r.get("instrument_id"),
            "underlying": parsed["underlying"],
            "expiration": parsed["expiration"],
            "right": parsed["right"],
            "strike": parsed["strike"],
        })
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.drop_duplicates("raw_symbol").sort_values(["expiration", "strike", "right"]).reset_index(drop=True)
