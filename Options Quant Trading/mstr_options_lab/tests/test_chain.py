"""Chain-level Greek tests.

Verifies that:
- compute_chain_greeks adds all 15 Greek columns
- vectorized values match per-row analytical bs_greeks
- enrich_chain_with_quotes on the sample chain produces a fully-populated table
"""

from __future__ import annotations

from datetime import date
import unittest

import numpy as np
import pandas as pd

from mstr_options_lab.greeks.analytical import bs_greeks
from mstr_options_lab.greeks.chain import compute_chain_greeks, ALL_GREEK_COLUMNS
from mstr_options_lab.pricing.black_scholes import bs_price


class TestChainGreeks(unittest.TestCase):
    def setUp(self):
        self.spot = 450.0
        self.rate = 0.045
        self.q = 0.0
        # Build a synthetic chain at a known IV; mid-price IS the BSM price at σ=0.85
        strikes = np.array([300.0, 350.0, 400.0, 450.0, 500.0, 550.0, 600.0])
        sigma = 0.85
        years = 30 / 365.0
        rows = []
        for K in strikes:
            for right in ("call", "put"):
                px = float(bs_price(self.spot, K, years, self.rate, sigma, right, self.q))
                rows.append({
                    "raw_symbol": f"MSTR_{int(K):04d}_{right[0].upper()}",
                    "strike": K,
                    "right": right,
                    "days_to_expiry": 30,
                    "mid": px,
                    "expiration": date(2026, 6, 14),
                })
        self.chain = pd.DataFrame(rows)

    def test_all_columns_added(self):
        out = compute_chain_greeks(self.chain, spot=self.spot, rate=self.rate, dividend_yield=self.q)
        for col in ["iv"] + ALL_GREEK_COLUMNS:
            self.assertIn(col, out.columns)
            self.assertEqual(out[col].notna().sum(), len(out), f"{col} has nulls")

    def test_iv_recovered(self):
        out = compute_chain_greeks(self.chain, spot=self.spot, rate=self.rate, dividend_yield=self.q)
        np.testing.assert_allclose(out["iv"].to_numpy(), 0.85, atol=1e-5)

    def test_matches_row_by_row(self):
        out = compute_chain_greeks(self.chain, spot=self.spot, rate=self.rate, dividend_yield=self.q)
        for _, row in out.iterrows():
            ref = bs_greeks(
                self.spot, row["strike"], 30 / 365.0, self.rate, row["iv"],
                row["right"], self.q,
            )
            for col in ["delta", "gamma", "vega", "theta", "vanna", "charm", "vomma", "speed", "zomma", "ultima"]:
                self.assertAlmostEqual(float(row[col]), float(getattr(ref, col)), places=8, msg=col)

    def test_put_call_symmetries(self):
        out = compute_chain_greeks(self.chain, spot=self.spot, rate=self.rate, dividend_yield=self.q)
        # group by strike, expect gamma/vega/vomma/vanna/veta/speed/zomma/color same for call vs put
        for K, sub in out.groupby("strike"):
            c = sub[sub["right"] == "call"].iloc[0]
            p = sub[sub["right"] == "put"].iloc[0]
            for col in ["gamma", "vega", "vomma", "vanna", "veta", "speed", "zomma", "color", "ultima"]:
                self.assertAlmostEqual(float(c[col]), float(p[col]), places=8, msg=f"{col} at K={K}")
            # delta_call - delta_put = e^{-qT}  (= 1 with q=0)
            self.assertAlmostEqual(float(c["delta"]) - float(p["delta"]), 1.0, places=8)


class TestEnrichWithSampleChain(unittest.TestCase):
    def test_enrich_sample_mstr_chain(self):
        from databento_options import sample_mstr_chain, enrich_chain_with_quotes
        as_of = date(2026, 5, 15)
        # Sample chain centered on spot=450 ensures the strike grid surrounds the
        # spot used for IV inversion — otherwise deep wing strikes produce NaN IV.
        spot = 450.0
        out = enrich_chain_with_quotes(
            sample_mstr_chain(as_of, spot=spot), pd.DataFrame(),
            spot=spot, rate=0.045, as_of=as_of,
        )
        for col in ["iv"] + ALL_GREEK_COLUMNS:
            self.assertIn(col, out.columns)
        # No nulls in any Greek for the sample chain (synthetic BSM prices invert cleanly)
        self.assertEqual(out["iv"].notna().sum(), len(out))
        self.assertEqual(out["vanna"].notna().sum(), len(out))


if __name__ == "__main__":
    unittest.main()
