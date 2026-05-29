"""Tests for the IBKR adapter — schema and helpers only.

We don't test the actual TWS connection here (no socket in CI). The integration
test path lives in `mstr_options_workstation.py` and runs end-to-end against a
live TWS Paper Trading session when the user selects "IBKR" as data source.
"""

from __future__ import annotations

import math
import unittest
from datetime import date

from mstr_options_lab.data.ibkr import (
    IBKRClient, IBKRConfig, IB_INSYNC_AVAILABLE, _occ_symbol, _safe_float,
)


class TestIBHelpers(unittest.TestCase):
    def test_occ_symbol_matches_databento_format(self):
        # Same OPRA format as Databento returns
        sym = _occ_symbol("MSTR", date(2026, 1, 16), "call", 500.0)
        self.assertEqual(sym, "MSTR  260116C00500000")
        sym_p = _occ_symbol("MSTR", date(2026, 6, 14), "put", 425.5)
        self.assertEqual(sym_p, "MSTR  260614P00425500")

    def test_safe_float_handles_ib_quirks(self):
        # IB returns NaN, None, -1 for missing data; normalize them all
        self.assertTrue(math.isnan(_safe_float(float("nan"))))
        self.assertTrue(math.isnan(_safe_float(None)))
        self.assertTrue(math.isnan(_safe_float(-1)))
        self.assertEqual(_safe_float(123.45), 123.45)
        self.assertEqual(_safe_float(0.0), 0.0)


@unittest.skipUnless(IB_INSYNC_AVAILABLE, "ib_insync not installed (optional broker SDK)")
class TestIBKRClientImport(unittest.TestCase):
    def test_ib_insync_available(self):
        self.assertTrue(IB_INSYNC_AVAILABLE, "ib_insync should be importable for this test environment")

    def test_client_construction_does_not_connect(self):
        # Constructor should NOT open a socket
        client = IBKRClient(IBKRConfig(host="127.0.0.1", port=7497, client_id=99))
        self.assertFalse(client._connected)


if __name__ == "__main__":
    unittest.main()
