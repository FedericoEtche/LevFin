"""Tests for the chain → implied distribution pipeline."""

from __future__ import annotations

import math
import unittest
from datetime import date, timedelta

import numpy as np
import pandas as pd

from mstr_options_lab.implied_dist import (
    compute_implied_distribution,
    slice_to_otm_smile,
)
from mstr_options_lab.pricing.black_scholes import bs_price


def _build_synthetic_chain(spot: float, sigma: float, rate: float, expiry: date, as_of: date, strikes=None):
    """Generate a chain at known IV — useful so we can compare recovered moments against the lognormal truth."""
    strikes = strikes if strikes is not None else np.arange(0.5, 1.55, 0.10) * spot
    years = max((expiry - as_of).days, 1) / 365.0
    rows = []
    for K in strikes:
        for right in ("call", "put"):
            mid = float(bs_price(spot, K, years, rate, sigma, right, 0.0))
            rows.append({
                "raw_symbol": f"TEST_{int(K):05d}_{right[0].upper()}",
                "expiration": expiry,
                "right": right,
                "strike": float(K),
                "days_to_expiry": (expiry - as_of).days,
                "mid": mid,
                "bid_px_00": mid - 0.05,
                "ask_px_00": mid + 0.05,
                "iv": sigma,  # set IV directly so we don't depend on the solver here
            })
    return pd.DataFrame(rows)


class TestSliceToOTMSmile(unittest.TestCase):
    def test_picks_correct_side(self):
        as_of = date(2026, 5, 15)
        expiry = as_of + timedelta(days=30)
        spot = 100.0
        chain = _build_synthetic_chain(spot, sigma=0.3, rate=0.04, expiry=expiry, as_of=as_of)
        F = spot * math.exp(0.04 * 30 / 365.0)
        k, iv = slice_to_otm_smile(chain, expiry, forward=F)
        # n strikes after OTM filter == number of strikes (one side per strike)
        self.assertEqual(k.size, chain["strike"].nunique())
        self.assertEqual(iv.size, k.size)
        np.testing.assert_allclose(iv, 0.3, atol=1e-8)


class TestImpliedDistribution(unittest.TestCase):
    def test_recovers_lognormal_moments(self):
        as_of = date(2026, 5, 15)
        expiry = as_of + timedelta(days=60)
        spot = 100.0
        sigma = 0.30
        rate = 0.04
        # Wide strike range so the right tail doesn't get truncated
        strikes = np.arange(0.30, 2.55, 0.05) * spot
        chain = _build_synthetic_chain(spot, sigma, rate, expiry, as_of, strikes=strikes)

        dist = compute_implied_distribution(chain, expiry, spot=spot, rate=rate, as_of=as_of)

        T = 60 / 365.0
        F_true = spot * math.exp(rate * T)
        self.assertAlmostEqual(dist.forward, F_true, places=6)
        self.assertAlmostEqual(dist.atm_iv, sigma, delta=0.02)
        # Lognormal mean = F
        self.assertAlmostEqual(dist.mean, F_true, delta=0.5)
        # Lognormal std = F · sqrt(e^{σ²T} - 1)  (analytical for lognormal moments)
        expected_std = F_true * math.sqrt(math.exp(sigma ** 2 * T) - 1)
        self.assertAlmostEqual(dist.std, expected_std, delta=expected_std * 0.05)
        # Skew of lognormal with σ√T = 0.0775: (e^{σ²T} + 2)·sqrt(e^{σ²T} - 1) ≈ 0.235
        sT = sigma * math.sqrt(T)
        expected_skew = (math.exp(sT ** 2) + 2) * math.sqrt(math.exp(sT ** 2) - 1)
        self.assertAlmostEqual(dist.skew, expected_skew, delta=0.1)
        # Density integrates to 1
        area = float(np.trapezoid(dist.pdf, dist.K))
        self.assertAlmostEqual(area, 1.0, delta=1e-3)
        # CDF endpoints
        self.assertAlmostEqual(float(dist.cdf[0]), 0.0, places=6)
        self.assertAlmostEqual(float(dist.cdf[-1]), 1.0, places=6)
        # Percentiles ordered
        self.assertLess(dist.p5, dist.p25)
        self.assertLess(dist.p25, dist.p50)
        self.assertLess(dist.p50, dist.p75)
        self.assertLess(dist.p75, dist.p95)

    def test_insufficient_strikes_raises(self):
        as_of = date(2026, 5, 15)
        expiry = as_of + timedelta(days=30)
        # Only 3 strikes — should fail (< 5 required)
        chain = _build_synthetic_chain(100.0, 0.3, 0.04, expiry, as_of, strikes=[90.0, 100.0, 110.0])
        with self.assertRaises(ValueError):
            compute_implied_distribution(chain, expiry, spot=100.0, rate=0.04, as_of=as_of)


if __name__ == "__main__":
    unittest.main()
