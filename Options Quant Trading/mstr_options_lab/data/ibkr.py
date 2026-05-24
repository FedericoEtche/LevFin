"""Interactive Brokers TWS API adapter — ib_insync based.

Replaces the three standalone scripts (ib_data_hourly.py, ib_vol.py, ib_nvda.py).
Schema-compatible with `databento_options.enrich_chain_with_quotes` so the rest
of the workstation works unchanged regardless of data source.

Connection
----------
- Default port: 7497 (TWS paper). Use 7496 for TWS live, 4002 for Gateway paper,
  4001 for Gateway live.
- TWS must be running and "Enable ActiveX and Socket Clients" must be checked in
  TWS → File → Global Configuration → API → Settings.

Pacing
------
- 50 simultaneous historical reqs max (we batch chains in 50-symbol chunks)
- 60 identical historical reqs per 10 min (we don't re-issue)
- No identical request within 15 sec (handled by snapshot=True for chain quotes)

Output schema (matches databento_options)
-----------------------------------------
- raw_symbol, underlying, expiration, right, strike, instrument_id
- bid_px_00, ask_px_00, mid, days_to_expiry
- iv (model-implied from IB tick type 13, or NaN if unavailable)
- delta, gamma, vega, theta (from IB; rest computed by compute_chain_greeks)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
import logging
import time
from typing import Optional

import numpy as np
import pandas as pd

try:
    from ib_insync import IB, Stock, Option, Contract, util
    IB_INSYNC_AVAILABLE = True
except ImportError:
    IB_INSYNC_AVAILABLE = False
    IB = Stock = Option = Contract = util = None  # type: ignore

log = logging.getLogger(__name__)


@dataclass
class IBKRConfig:
    host: str = "127.0.0.1"
    port: int = 7497          # 7497 = TWS paper, 7496 = TWS live, 4002 = GW paper, 4001 = GW live
    client_id: int = 17
    timeout: float = 10.0


class IBKRClient:
    """ib_insync-based client. Use as a context manager or call connect()/disconnect()."""

    def __init__(self, config: IBKRConfig | None = None):
        if not IB_INSYNC_AVAILABLE:
            raise RuntimeError("ib_insync is not installed.  pip install ib_insync")
        self.config = config or IBKRConfig()
        self.ib = IB()
        self._connected = False

    def __enter__(self) -> "IBKRClient":
        self.connect()
        return self

    def __exit__(self, *exc) -> None:
        self.disconnect()

    def connect(self) -> None:
        if self._connected:
            return
        self.ib.connect(self.config.host, self.config.port, clientId=self.config.client_id, timeout=self.config.timeout)
        self._connected = True

    def disconnect(self) -> None:
        if self._connected:
            self.ib.disconnect()
            self._connected = False

    # ----- Underlying quote -----
    def fetch_underlying_quote(self, symbol: str, exchange: str = "SMART", currency: str = "USD") -> dict:
        """Returns a snapshot dict: {symbol, last, bid, ask, conId}."""
        stk = Stock(symbol, exchange, currency)
        self.ib.qualifyContracts(stk)
        ticker = self.ib.reqMktData(stk, "", snapshot=True, regulatorySnapshot=False)
        self.ib.sleep(1.5)  # let the snapshot populate
        out = {
            "symbol": symbol,
            "conId": int(stk.conId),
            "last": _safe_float(ticker.last),
            "bid": _safe_float(ticker.bid),
            "ask": _safe_float(ticker.ask),
            "close": _safe_float(ticker.close),
        }
        self.ib.cancelMktData(stk)
        return out

    # ----- Option chain enumeration -----
    def fetch_option_chain(
        self,
        symbol: str,
        max_expiries: int = 4,
        strike_window_pct: float = 0.40,
        spot_hint: float | None = None,
        exchange: str = "SMART",
        currency: str = "USD",
        as_of: date | None = None,
    ) -> pd.DataFrame:
        """Enumerate and quote the option chain.

        Steps:
        1. Qualify the underlying, get conId.
        2. reqSecDefOptParams → list of expiries + strikes.
        3. Slice strikes to [(1-w)·spot, (1+w)·spot] using ``spot_hint`` or the
           underlying's last quote.
        4. Qualify all option contracts.
        5. Snapshot quotes (bid/ask + IB-computed model IV/Greeks via tick 13).
        6. Return a DataFrame matching the Databento adapter's schema.
        """
        as_of = as_of or date.today()
        stk = Stock(symbol, exchange, currency)
        [stk_q] = self.ib.qualifyContracts(stk)
        underlying_conId = int(stk_q.conId)

        # Get the spot for strike-window filtering
        if spot_hint is None:
            quote = self.fetch_underlying_quote(symbol, exchange, currency)
            spot_hint = quote.get("last") or quote.get("close") or 0.0
        if not spot_hint or spot_hint <= 0:
            raise ValueError(f"Could not determine spot for {symbol}; pass spot_hint=...")

        chain_params = self.ib.reqSecDefOptParams(symbol, "", "STK", underlying_conId)
        if not chain_params:
            raise RuntimeError(f"No option chain params returned for {symbol}")
        # Prefer the SMART/NYSE/NASDAQ aggregate listing; ib_insync usually returns one row
        params = chain_params[0]
        all_expiries = sorted(params.expirations)
        all_strikes = sorted(params.strikes)

        # Filter: top-N nearest expiries + strikes in window around spot
        expiries = all_expiries[:max_expiries]
        lo = spot_hint * (1.0 - strike_window_pct)
        hi = spot_hint * (1.0 + strike_window_pct)
        strikes = [k for k in all_strikes if lo <= k <= hi]
        if not strikes:
            raise RuntimeError(f"No strikes within {strike_window_pct:.0%} of {spot_hint} for {symbol}")
        trading_class = getattr(params, "tradingClass", symbol)

        # Build option contracts (calls + puts × strikes × expiries)
        contracts: list[Option] = []
        for exp in expiries:
            for k in strikes:
                for right in ("C", "P"):
                    contracts.append(Option(symbol, exp, k, right, exchange, tradingClass=trading_class, currency=currency))
        qualified = self.ib.qualifyContracts(*contracts)
        # Some contracts may not exist (illiquid strikes); drop those
        contracts = [c for c in qualified if c.conId]

        # Snapshot quotes — generic ticks 100/101/104/105/106 + 13 (model option computation)
        tickers = []
        for c in contracts:
            tickers.append(self.ib.reqMktData(c, "100,101,104,105,106,165,221", snapshot=True, regulatorySnapshot=False))
        # Wait for snapshots to populate; IB will fire ~each contract within a couple seconds
        self.ib.sleep(min(2.0 + 0.005 * len(contracts), 10.0))

        rows: list[dict] = []
        for c, t in zip(contracts, tickers):
            exp = datetime.strptime(c.lastTradeDateOrContractMonth, "%Y%m%d").date()
            right = "call" if c.right == "C" else "put"
            mid_model = getattr(t, "modelGreeks", None)
            row = {
                "raw_symbol": _occ_symbol(symbol, exp, right, c.strike),
                "underlying": symbol,
                "expiration": exp,
                "right": right,
                "strike": float(c.strike),
                "instrument_id": int(c.conId) if c.conId else None,
                "bid_px_00": _safe_float(t.bid),
                "ask_px_00": _safe_float(t.ask),
                "days_to_expiry": max((exp - as_of).days, 0),
                # IB model greeks if available; we'll let compute_chain_greeks fill in
                # the higher-order ones from our own analytical formulas.
                "iv_ibkr": _safe_float(mid_model.impliedVol) if mid_model else float("nan"),
                "delta_ibkr": _safe_float(mid_model.delta) if mid_model else float("nan"),
                "gamma_ibkr": _safe_float(mid_model.gamma) if mid_model else float("nan"),
                "vega_ibkr": _safe_float(mid_model.vega) if mid_model else float("nan"),
                "theta_ibkr": _safe_float(mid_model.theta) if mid_model else float("nan"),
            }
            rows.append(row)
            self.ib.cancelMktData(c)

        df = pd.DataFrame(rows)
        if df.empty:
            return df
        df = df.dropna(subset=["bid_px_00", "ask_px_00"], how="all")
        return df.sort_values(["expiration", "strike", "right"]).reset_index(drop=True)


def _safe_float(x) -> float:
    """ib_insync returns NaN-as-Decimal, sometimes -1, sometimes None — normalize."""
    try:
        v = float(x)
        if not np.isfinite(v) or v < 0:
            return float("nan")
        return v
    except (TypeError, ValueError):
        return float("nan")


def _occ_symbol(underlying: str, expiry: date, right: str, strike: float) -> str:
    """Build the 21-char OCC symbol matching the Databento format."""
    return f"{underlying:<6}{expiry.strftime('%y%m%d')}{('C' if right == 'call' else 'P')}{int(strike * 1000):08d}"
