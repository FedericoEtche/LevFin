"""Tests for the Databento Live adapter — helpers only.

The actual Live API path is exercised manually via the workstation against
real OPRA market data. These tests cover the offline-verifiable surface:
construction, OCC normalization, and graceful failure when the key is missing.
"""

from __future__ import annotations

import os
import unittest
from datetime import date

import pandas as pd

from mstr_options_lab.data.databento_live import (
    DatabentoLiveClient,
    DatabentoLiveConfig,
    _normalize_definitions,
    DEFAULT_EQUITY_DATASET,
    DEFAULT_OPTIONS_DATASET,
    FIXED_PRICE_SCALE,
)


class TestDefaults(unittest.TestCase):
    def test_default_datasets(self):
        self.assertEqual(DEFAULT_EQUITY_DATASET, "EQUS.MINI")
        self.assertEqual(DEFAULT_OPTIONS_DATASET, "OPRA.PILLAR")

    def test_price_scale(self):
        # Databento DBN convention: int64 prices × 1e9 = decimal
        self.assertEqual(FIXED_PRICE_SCALE, 1_000_000_000.0)


class TestConstructorErrors(unittest.TestCase):
    def test_missing_key_raises(self):
        saved = os.environ.pop("DATABENTO_API_KEY", None)
        try:
            with self.assertRaises(RuntimeError) as ctx:
                DatabentoLiveClient(DatabentoLiveConfig(api_key=None))
            self.assertIn("DATABENTO_API_KEY", str(ctx.exception))
        finally:
            if saved is not None:
                os.environ["DATABENTO_API_KEY"] = saved

    def test_explicit_key_overrides_env(self):
        client = DatabentoLiveClient(DatabentoLiveConfig(api_key="db-test-12345"))
        self.assertEqual(client.api_key, "db-test-12345")


class TestNormalizeDefinitions(unittest.TestCase):
    def test_parses_occ_and_drops_garbage(self):
        df = pd.DataFrame([
            {"raw_symbol": "MSTR  260116C00500000", "instrument_id": 100},
            {"raw_symbol": "MSTR  260116P00500000", "instrument_id": 101},
            {"raw_symbol": "garbage-not-occ",       "instrument_id": 999},
            {"raw_symbol": "MSTR  260116C00500000", "instrument_id": 100},  # dup
        ])
        out = _normalize_definitions(df)
        self.assertEqual(len(out), 2)  # 1 call, 1 put, dup dropped, garbage dropped
        self.assertSetEqual(set(out["right"]), {"call", "put"})
        self.assertEqual(out.iloc[0]["expiration"], date(2026, 1, 16))
        self.assertEqual(out.iloc[0]["strike"], 500.0)

    def test_empty_input(self):
        out = _normalize_definitions(pd.DataFrame())
        self.assertTrue(out.empty)


if __name__ == "__main__":
    unittest.main()
