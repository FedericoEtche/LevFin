"""End-to-end math correctness tests.

These are intentionally written to be runnable WITHOUT any external data or
network calls — they validate the theoretical core only.

Run:
    cd "Options Quant Trading"
    python -m unittest mstr_options_lab.tests.test_math -v
"""

from __future__ import annotations

import math
import unittest

import numpy as np

from mstr_options_lab.pricing.black_scholes import bs_price, bs_implied_vol
from mstr_options_lab.pricing.characteristic_fns import (
    bsm_cf,
    heston_cf,
    merton_cf,
    variance_gamma_cf,
    HestonParams,
    MertonParams,
    VGParams,
)
from mstr_options_lab.pricing.carr_madan import fft_price_one, fft_call_prices, fft_prices_many_strikes
from mstr_options_lab.greeks.analytical import bs_greeks
from mstr_options_lab.greeks.numerical import fd_greeks
from mstr_options_lab.surface.svi import fit_svi_slice, svi_iv, SVIParams
from mstr_options_lab.implied_dist.breeden_litzenberger import (
    risk_neutral_pdf_from_calls,
    risk_neutral_pdf_from_svi,
    risk_neutral_cdf,
)


S0 = 100.0
K = 100.0
T = 1.0
R = 0.03
Q = 0.0
SIG = 0.25


class TestBlackScholes(unittest.TestCase):
    def test_atm_call_vs_known_value(self):
        # ATM, r=0.03, q=0, σ=0.25, T=1, S=K=100 → ~11.0  (Hull table)
        price = float(bs_price(S0, K, T, R, SIG, "call", Q))
        self.assertAlmostEqual(price, 11.0, delta=0.5)

    def test_put_call_parity(self):
        c = float(bs_price(S0, K, T, R, SIG, "call", Q))
        p = float(bs_price(S0, K, T, R, SIG, "put", Q))
        lhs = c - p
        rhs = S0 * math.exp(-Q * T) - K * math.exp(-R * T)
        self.assertAlmostEqual(lhs, rhs, places=10)

    def test_iv_roundtrip(self):
        true_sigma = 0.37
        c = float(bs_price(S0, K, T, R, true_sigma, "call", Q))
        iv = float(bs_implied_vol(c, S0, K, T, R, "call", Q))
        self.assertAlmostEqual(iv, true_sigma, places=6)

    def test_vectorized_pricing(self):
        strikes = np.array([80.0, 90.0, 100.0, 110.0, 120.0])
        prices = bs_price(S0, strikes, T, R, SIG, "call", Q)
        # monotone non-increasing in K for calls
        self.assertTrue(np.all(np.diff(prices) <= 0))


class TestCarrMadan(unittest.TestCase):
    def test_bsm_cf_matches_closed_form(self):
        """Carr-Madan with the BSM CF must agree with analytical BSM."""
        c_fft = fft_price_one(bsm_cf, S0, K, T, R, Q, params=SIG, right="call")
        c_bs = float(bs_price(S0, K, T, R, SIG, "call", Q))
        self.assertAlmostEqual(c_fft, c_bs, delta=0.05)

    def test_heston_fft_sanity(self):
        hp = HestonParams(kappa=1.5, theta=0.04, sigma=0.3, rho=-0.7, v0=0.04)
        c = fft_price_one(heston_cf, S0, 100.0, T, R, Q, hp)
        # Heston with v0=θ=0.04 ≈ flat σ=20% → ATM call ≈ 8.92
        self.assertGreater(c, 6.0)
        self.assertLess(c, 12.0)

    def test_put_call_parity_via_fft(self):
        hp = HestonParams(kappa=1.5, theta=0.04, sigma=0.3, rho=-0.7, v0=0.04)
        c = fft_price_one(heston_cf, S0, 100.0, T, R, Q, hp, right="call")
        p = fft_price_one(heston_cf, S0, 100.0, T, R, Q, hp, right="put")
        lhs = c - p
        rhs = S0 * math.exp(-Q * T) - 100.0 * math.exp(-R * T)
        self.assertAlmostEqual(lhs, rhs, delta=0.02)

    def test_merton_cf_runs(self):
        mp = MertonParams(sigma=0.2, lam=0.5, mu_j=-0.05, sigma_j=0.15)
        c = fft_price_one(merton_cf, S0, K, T, R, Q, mp)
        # Merton with jumps should price ATM call near BSM-σ=0.25 zone (≈11) but skewed
        self.assertGreater(c, 5.0)
        self.assertLess(c, 20.0)

    def test_vg_cf_runs(self):
        vp = VGParams(sigma=0.2, nu=0.5, theta=-0.1)
        c = fft_price_one(variance_gamma_cf, S0, K, T, R, Q, vp)
        self.assertGreater(c, 5.0)
        self.assertLess(c, 20.0)


class TestGreeks(unittest.TestCase):
    def test_analytical_matches_finite_diff(self):
        """All 15 BSM Greeks should agree with central-difference estimates."""
        g_an = bs_greeks(S0, K, T, R, SIG, "call", Q)

        def pricer(S, K_, T_, r_, q_, **kw):
            sigma_ = kw.get("vol", SIG)
            return float(bs_price(S, K_, T_, r_, sigma_, "call", q_))

        g_fd = fd_greeks(pricer, S0, K, T, R, Q, sigma_arg="vol", vol=SIG)
        # 1st order
        self.assertAlmostEqual(float(g_an.delta), g_fd["delta"], places=4)
        self.assertAlmostEqual(float(g_an.gamma), g_fd["gamma"], places=4)
        self.assertAlmostEqual(float(g_an.vega), g_fd["vega"], places=3)
        self.assertAlmostEqual(float(g_an.theta), g_fd["theta"], delta=1e-2)
        self.assertAlmostEqual(float(g_an.rho), g_fd["rho"], places=2)
        self.assertAlmostEqual(float(g_an.epsilon), g_fd["epsilon"], delta=1e-2)
        # 2nd order
        self.assertAlmostEqual(float(g_an.vanna), g_fd["vanna"], delta=1e-2)
        self.assertAlmostEqual(float(g_an.vomma), g_fd["vomma"], delta=1e-1)
        self.assertAlmostEqual(float(g_an.charm), g_fd["charm"], delta=1e-3)
        self.assertAlmostEqual(float(g_an.veta), g_fd["veta"], delta=1.0)
        self.assertAlmostEqual(float(g_an.vera), g_fd["vera"], delta=1.0)
        # 3rd order
        self.assertAlmostEqual(float(g_an.speed), g_fd["speed"], delta=1e-3)
        self.assertAlmostEqual(float(g_an.zomma), g_fd["zomma"], delta=1e-2)
        self.assertAlmostEqual(float(g_an.color), g_fd["color"], delta=1e-3)
        self.assertAlmostEqual(float(g_an.ultima), g_fd["ultima"], delta=2.0)

    def test_put_call_greek_relations(self):
        g_c = bs_greeks(S0, K, T, R, SIG, "call", Q)
        g_p = bs_greeks(S0, K, T, R, SIG, "put", Q)
        # delta_c - delta_p = e^{-qT}
        self.assertAlmostEqual(
            float(g_c.delta) - float(g_p.delta), math.exp(-Q * T), places=10
        )
        # gamma_c == gamma_p, vega_c == vega_p, vomma_c == vomma_p
        self.assertAlmostEqual(float(g_c.gamma), float(g_p.gamma), places=10)
        self.assertAlmostEqual(float(g_c.vega), float(g_p.vega), places=10)
        self.assertAlmostEqual(float(g_c.vomma), float(g_p.vomma), places=10)
        self.assertAlmostEqual(float(g_c.vanna), float(g_p.vanna), places=10)

    def test_vectorized_greeks(self):
        strikes = np.array([80.0, 90.0, 100.0, 110.0, 120.0])
        g = bs_greeks(S0, strikes, T, R, SIG, "call", Q)
        self.assertEqual(g.delta.shape, strikes.shape)
        # Call deltas monotone in K
        self.assertTrue(np.all(np.diff(g.delta) <= 0))


class TestImpliedDistribution(unittest.TestCase):
    def test_bl_recovers_lognormal_under_bsm(self):
        """Under BSM with constant σ, the implied density should be lognormal.

        Use a wide K range so the right tail isn't truncated — naïve BL on a
        narrow grid will bias E[S_T] downward.
        """
        K_grid = np.linspace(1.0, 600.0, 1201)
        C = bs_price(S0, K_grid, T, R, SIG, "call", Q)
        pdf = risk_neutral_pdf_from_calls(K_grid, np.asarray(C), r=R, T=T)
        # Density should integrate to (approximately) 1
        area = float(np.trapezoid(pdf, K_grid))
        self.assertAlmostEqual(area, 1.0, delta=0.005)
        # Mean ≈ S0·e^{(r-q)T} = 103.045
        mean = float(np.trapezoid(K_grid * pdf, K_grid))
        self.assertAlmostEqual(mean, S0 * math.exp((R - Q) * T), delta=0.1)
        # Mode of lognormal should be below the mean
        mode_K = float(K_grid[np.argmax(pdf)])
        self.assertLess(mode_K, mean)

    def test_pdf_via_svi_pipeline(self):
        # Build a synthetic smile from a known BSM σ, fit SVI, derive PDF
        K_obs = np.linspace(60.0, 160.0, 21)
        sigma_obs = np.full_like(K_obs, SIG) + 0.05 * (
            (K_obs - S0) / S0
        ) ** 2  # mild U-shape
        F = S0 * math.exp((R - Q) * T)
        k_obs = np.log(K_obs / F)
        svi = fit_svi_slice(k_obs, sigma_obs, T=T)
        self.assertGreater(svi.b, 0)
        self.assertLess(abs(svi.rho), 1)
        K_grid, pdf = risk_neutral_pdf_from_svi(S0, svi, T, R, Q)
        area = float(np.trapezoid(pdf, K_grid))
        self.assertAlmostEqual(area, 1.0, delta=1e-3)

    def test_cdf_monotone(self):
        K_grid = np.linspace(40.0, 200.0, 401)
        C = bs_price(S0, K_grid, T, R, SIG, "call", Q)
        pdf = risk_neutral_pdf_from_calls(K_grid, np.asarray(C), r=R, T=T)
        cdf = risk_neutral_cdf(K_grid, pdf)
        self.assertTrue(np.all(np.diff(cdf) >= -1e-12))
        self.assertAlmostEqual(cdf[0], 0.0, delta=1e-6)
        self.assertAlmostEqual(cdf[-1], 1.0, delta=1e-6)


if __name__ == "__main__":
    unittest.main()
