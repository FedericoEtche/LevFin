from __future__ import annotations

from datetime import date
import unittest

from options_quant_desktop import analytics


class OptionsQuantDesktopTests(unittest.TestCase):
    def test_sample_chain_has_advanced_greeks(self):
        chain = analytics.load_sample_chain(
            underlying="MSTR",
            spot=450.0,
            rate=0.045,
            dividend_yield=0.0,
            as_of=date(2026, 5, 15),
        )

        self.assertFalse(chain.empty)
        for col in ["iv", "delta", "gamma", "vega_1pct", "vanna_1pct", "volga_1pct2", "color_day"]:
            self.assertIn(col, chain.columns)
        self.assertGreater(chain["iv"].dropna().mean(), 0)

    def test_smile_and_distribution_from_sample_chain(self):
        chain = analytics.load_sample_chain(
            underlying="MSTR",
            spot=450.0,
            rate=0.045,
            dividend_yield=0.0,
            as_of=date(2026, 5, 15),
        )
        expiry = analytics.available_expirations(chain)[0]

        smile = analytics.fit_smile(chain, expiry, 450.0, 0.045, 0.0, date(2026, 5, 15))
        self.assertGreater(len(smile.curve), 100)
        self.assertGreater(smile.forward, 0)

        dist = analytics.implied_distribution(chain, expiry, 450.0, 0.045, 0.0, date(2026, 5, 15))
        self.assertGreater(len(dist.grid), 1000)
        self.assertGreater(dist.mean, 0)
        self.assertGreaterEqual(dist.prob_below_spot, 0)
        self.assertLessEqual(dist.prob_below_spot, 1)

    def test_model_price_table_runs(self):
        prices = analytics.model_price_table(
            spot=450.0,
            strike=450.0,
            days_to_expiry=30,
            rate=0.045,
            dividend_yield=0.0,
            vol=0.85,
            right="call",
        )

        self.assertEqual(len(prices), 5)
        self.assertTrue((prices["price"] > 0).all())


if __name__ == "__main__":
    unittest.main()
