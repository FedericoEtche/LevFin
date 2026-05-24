"""Heston calibration + Heston-implied PDF tests.

Strategy: build a synthetic chain priced at known constant σ (BSM lognormal),
calibrate Heston, expect θ ≈ σ², v0 ≈ σ², σ_volvol ≈ 0, RMSE ≈ 0.

Then verify the Heston-implied PDF for that surface matches the lognormal of
the same σ in mean / std / area.
"""

from __future__ import annotations

import math
import unittest
from datetime import date, timedelta

import numpy as np
import pandas as pd

from mstr_options_lab.pricing import calibrate_heston
from mstr_options_lab.implied_dist import heston_pdf_for_expiry
from mstr_options_lab.greeks.chain import compute_chain_greeks
from mstr_options_lab.tests.test_implied_dist import _build_synthetic_chain


class TestHestonCalibration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.as_of = date(2026, 5, 15)
        cls.spot = 100.0
        cls.sigma = 0.30
        cls.rate = 0.04
        strikes = np.arange(0.5, 1.55, 0.05) * cls.spot
        parts = []
        for days in (30, 60, 90):
            exp = cls.as_of + timedelta(days=days)
            parts.append(_build_synthetic_chain(cls.spot, cls.sigma, cls.rate, exp, cls.as_of, strikes=strikes))
        cls.chain = compute_chain_greeks(
            pd.concat(parts, ignore_index=True),
            spot=cls.spot, rate=cls.rate,
        )
        cls.result = calibrate_heston(
            cls.chain, spot=cls.spot, rate=cls.rate, as_of=cls.as_of, n_starts=3,
        )

    def test_recovers_flat_smile(self):
        # On a BSM-priced chain Heston should degenerate: θ ≈ v0 ≈ σ², σ_volvol → 0
        target = self.sigma ** 2
        self.assertAlmostEqual(self.result.params.theta, target, delta=0.02)
        self.assertAlmostEqual(self.result.params.v0, target, delta=0.02)
        self.assertLess(self.result.params.sigma, 0.15)  # vol-of-vol small

    def test_low_rmse(self):
        # Fit a BSM surface → calibration error should be near zero (well under 1 vol pt)
        self.assertLess(self.result.rmse_iv_pct, 1.0)

    def test_metadata(self):
        self.assertEqual(self.result.n_expiries, 3)
        self.assertGreater(self.result.n_options, 20)

    def test_heston_pdf_matches_lognormal(self):
        # Use the calibrated Heston to derive a PDF for the 30-day expiry,
        # compare to lognormal at σ=0.30
        T = 30 / 365.0
        F = self.spot * math.exp(self.rate * T)
        K, pdf, cdf = heston_pdf_for_expiry(
            self.spot, T, self.rate, 0.0, self.result.params,
            K_min=1.0, K_max=500.0, n_K=2001,
        )
        area = float(np.trapezoid(pdf, K))
        self.assertAlmostEqual(area, 1.0, delta=0.01)
        mean = float(np.trapezoid(K * pdf, K))
        self.assertAlmostEqual(mean, F, delta=0.5)
        var = float(np.trapezoid((K - mean) ** 2 * pdf, K))
        std = math.sqrt(var)
        expected_std = F * math.sqrt(math.exp(self.sigma ** 2 * T) - 1)
        # Heston with these recovered params should be within a few percent of lognormal
        self.assertAlmostEqual(std, expected_std, delta=expected_std * 0.1)
        # CDF endpoints
        self.assertAlmostEqual(float(cdf[0]), 0.0, places=4)
        self.assertAlmostEqual(float(cdf[-1]), 1.0, places=4)


if __name__ == "__main__":
    unittest.main()
