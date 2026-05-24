"""Optional IBKR/TWS bridge built on ib_insync.

The desktop app can open without TWS. This module is imported lazily by the UI
and raises clear runtime errors when ib_insync or TWS/Gateway are unavailable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import math
import time
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class IbkrConnection:
    host: str = "127.0.0.1"
    port: int = 7497
    client_id: int = 19


class IbkrBridge:
    def __init__(self) -> None:
        try:
            from ib_insync import IB
        except Exception as exc:  # pragma: no cover - depends on optional install
            raise RuntimeError("ib_insync is not installed.") from exc
        self._ib = IB()

    @property
    def connected(self) -> bool:
        return bool(self._ib.isConnected())

    def connect(self, config: IbkrConnection) -> None:
        if self.connected:
            return
        self._ib.connect(config.host, int(config.port), clientId=int(config.client_id), timeout=8)

    def disconnect(self) -> None:
        if self.connected:
            self._ib.disconnect()

    def stock_snapshot(self, symbol: str) -> float | None:
        from ib_insync import Stock

        if not self.connected:
            raise RuntimeError("IBKR is not connected.")
        contract = Stock(symbol.upper(), "SMART", "USD")
        self._ib.qualifyContracts(contract)
        ticker = self._ib.reqMktData(contract, "", True, False)
        for _ in range(40):
            self._ib.sleep(0.1)
            if ticker.marketPrice() == ticker.marketPrice() and not math.isnan(ticker.marketPrice() or float("nan")):
                break
        price = ticker.marketPrice()
        self._ib.cancelMktData(contract)
        return None if price is None or math.isnan(price) else float(price)

    def option_parameters(self, symbol: str) -> tuple[list[str], list[float], str, str]:
        from ib_insync import Stock

        if not self.connected:
            raise RuntimeError("IBKR is not connected.")
        stock = Stock(symbol.upper(), "SMART", "USD")
        self._ib.qualifyContracts(stock)
        if not stock.conId:
            raise RuntimeError(f"Could not qualify underlying contract for {symbol}.")

        params = self._ib.reqSecDefOptParams(symbol.upper(), "", "STK", stock.conId)
        if not params:
            raise RuntimeError(f"No option parameters returned for {symbol}.")

        # Prefer SMART, otherwise use the first returned chain.
        selected = next((p for p in params if p.exchange == "SMART"), params[0])
        expirations = sorted(str(exp) for exp in selected.expirations)
        strikes = sorted(float(strike) for strike in selected.strikes if float(strike) > 0)
        return expirations, strikes, selected.exchange, selected.tradingClass

    def option_snapshot_chain(
        self,
        symbol: str,
        spot: float,
        expirations: Iterable[str],
        strikes: Iterable[float],
        max_contracts: int = 60,
    ) -> pd.DataFrame:
        from ib_insync import Option

        if not self.connected:
            raise RuntimeError("IBKR is not connected.")

        max_contracts = max(int(max_contracts), 1)
        chosen_expirations = list(expirations)[:3]
        chosen_strikes = sorted(strikes, key=lambda strike: abs(float(strike) - float(spot)))[: max_contracts // 2]
        contracts = []
        for expiry in chosen_expirations:
            for strike in chosen_strikes:
                contracts.append(Option(symbol.upper(), expiry, float(strike), "C", "SMART", currency="USD"))
                contracts.append(Option(symbol.upper(), expiry, float(strike), "P", "SMART", currency="USD"))
                if len(contracts) >= max_contracts:
                    break
            if len(contracts) >= max_contracts:
                break

        qualified = self._ib.qualifyContracts(*contracts)
        tickers = [self._ib.reqMktData(contract, "", True, False) for contract in qualified]
        for _ in range(60):
            self._ib.sleep(0.1)
            valid = sum(1 for t in tickers if (t.bid is not None and not math.isnan(t.bid)) or (t.ask is not None and not math.isnan(t.ask)))
            if len(tickers) > 0 and valid >= len(tickers) * 0.9:
                break

        rows = []
        for ticker in tickers:
            contract = ticker.contract
            right = "call" if contract.right == "C" else "put"
            expiration = date(
                int(contract.lastTradeDateOrContractMonth[:4]),
                int(contract.lastTradeDateOrContractMonth[4:6]),
                int(contract.lastTradeDateOrContractMonth[6:8]),
            )
            bid = None if ticker.bid is None or math.isnan(ticker.bid) else float(ticker.bid)
            ask = None if ticker.ask is None or math.isnan(ticker.ask) else float(ticker.ask)
            model = ticker.modelGreeks
            rows.append(
                {
                    "raw_symbol": f"{symbol.upper()} {contract.lastTradeDateOrContractMonth} {contract.right} {contract.strike:g}",
                    "expiration": expiration,
                    "right": right,
                    "strike": float(contract.strike),
                    "bid_px_00": bid,
                    "ask_px_00": ask,
                    "ib_model_iv": None if model is None else model.impliedVol,
                    "ib_model_delta": None if model is None else model.delta,
                    "ib_model_gamma": None if model is None else model.gamma,
                    "ib_model_vega": None if model is None else model.vega,
                    "ib_model_theta": None if model is None else model.theta,
                }
            )
            self._ib.cancelMktData(contract)

        return pd.DataFrame(rows)
