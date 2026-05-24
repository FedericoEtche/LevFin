import math
import unittest

from options_core import (
    OptionLeg,
    black_scholes_price,
    implied_volatility,
    normalize_implied_vol,
    option_greeks,
    scenario_table,
    strategy_metrics,
    volatility_snapshot,
)


class OptionsCoreTests(unittest.TestCase):
    def test_black_scholes_known_values(self):
        call = black_scholes_price(100, 100, 1.0, 0.05, 0.20, "call")
        put = black_scholes_price(100, 100, 1.0, 0.05, 0.20, "put")

        self.assertAlmostEqual(call, 10.4506, places=4)
        self.assertAlmostEqual(put, 5.5735, places=4)

    def test_implied_volatility_recovers_input(self):
        target_vol = 0.32
        price = black_scholes_price(100, 105, 45 / 365, 0.04, target_vol, "call")
        recovered = implied_volatility(price, 100, 105, 45 / 365, 0.04, "call")

        self.assertAlmostEqual(recovered, target_vol, places=5)

    def test_normalize_implied_vol_units(self):
        self.assertAlmostEqual(normalize_implied_vol(0.25, "decimal_annual"), 0.25)
        self.assertAlmostEqual(normalize_implied_vol(25, "percent_annual"), 0.25)
        self.assertAlmostEqual(normalize_implied_vol(0.25, "auto_annual"), 0.25)
        self.assertAlmostEqual(normalize_implied_vol(25, "auto_annual"), 0.25)
        self.assertAlmostEqual(
            normalize_implied_vol(0.015, "decimal_daily"),
            0.015 * math.sqrt(252),
        )
        self.assertAlmostEqual(
            normalize_implied_vol(1.5, "percent_daily"),
            0.015 * math.sqrt(252),
        )

    def test_greeks_are_reasonable_for_atm_call(self):
        greeks = option_greeks(100, 100, 30 / 365, 0.05, 0.25, "call")

        self.assertGreater(greeks.delta, 0.45)
        self.assertLess(greeks.delta, 0.60)
        self.assertGreater(greeks.gamma, 0)
        self.assertGreater(greeks.vega, 0)
        self.assertLess(greeks.theta, 0)

    def test_strategy_metrics_for_long_straddle(self):
        legs = [OptionLeg("call", 100, 1), OptionLeg("put", 100, 1)]
        metrics = strategy_metrics(legs, 100, 30, 0.05, 0.25)

        self.assertGreater(metrics.value, 0)
        self.assertAlmostEqual(metrics.delta, option_greeks(100, 100, 30 / 365, 0.05, 0.25, "call").delta * 100 + option_greeks(100, 100, 30 / 365, 0.05, 0.25, "put").delta * 100)
        self.assertGreater(metrics.vega, 0)

    def test_scenario_table_long_straddle_gains_on_large_move(self):
        legs = [OptionLeg("call", 100, 1), OptionLeg("put", 100, 1)]
        rows = scenario_table(
            legs=legs,
            spot=100,
            days_to_expiry=30,
            rate=0.05,
            vol=0.25,
            spot_moves_pct=[0, 10],
            vol_moves_points=[0],
            days_elapsed=0,
        )
        pnl_by_move = {row["spot_move_pct"]: row["pnl"] for row in rows}

        self.assertAlmostEqual(pnl_by_move[0], 0.0, places=8)
        self.assertGreater(pnl_by_move[10], 0)

    def test_volatility_snapshot_flags_vrp(self):
        snap = volatility_snapshot(
            spot=100,
            current_iv=0.35,
            forecast_rv=0.22,
            days_to_expiry=30,
            iv_history=[0.15, 0.20, 0.25, 0.30, 0.35],
        )

        self.assertEqual(snap.screen, "short-vol candidate")
        self.assertGreater(snap.expected_move_1sigma, 0)


if __name__ == "__main__":
    unittest.main()
