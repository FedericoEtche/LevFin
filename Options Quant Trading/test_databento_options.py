from __future__ import annotations

from datetime import date
import unittest

import pandas as pd

from databento_options import enrich_chain_with_quotes, parent_symbol, parse_occ_symbol


class DatabentoOptionsTests(unittest.TestCase):
    def test_parent_symbol_for_mstr(self):
        self.assertEqual(parent_symbol("mstr"), "MSTR.OPT")

    def test_parse_occ_symbol(self):
        parsed = parse_occ_symbol("MSTR  260116C00500000")

        self.assertEqual(parsed["underlying"], "MSTR")
        self.assertEqual(parsed["expiration"], date(2026, 1, 16))
        self.assertEqual(parsed["right"], "call")
        self.assertEqual(parsed["strike"], 500.0)

    def test_enrich_chain_with_quotes_calculates_iv_and_greeks(self):
        definitions = pd.DataFrame(
            [
                {
                    "raw_symbol": "MSTR  260116C00500000",
                    "underlying": "MSTR",
                    "expiration": date(2026, 1, 16),
                    "right": "call",
                    "strike": 500.0,
                    "instrument_id": 1,
                }
            ]
        )
        quotes = pd.DataFrame(
            [
                {
                    "symbol": "MSTR  260116C00500000",
                    "bid_px_00": 54.0,
                    "ask_px_00": 56.0,
                }
            ]
        )

        chain = enrich_chain_with_quotes(
            definitions=definitions,
            quotes=quotes,
            spot=500.0,
            rate=0.04,
            as_of=date(2025, 12, 17),
        )

        self.assertAlmostEqual(chain.loc[0, "mid"], 55.0)
        self.assertGreater(chain.loc[0, "iv"], 0.0)
        self.assertGreater(chain.loc[0, "delta"], 0.0)


if __name__ == "__main__":
    unittest.main()
