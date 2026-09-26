import copy
import unittest

from foundations.td import estimate_values, update_value
from foundations.monte_carlo import estimate_values as monte_carlo


class TestTD(unittest.TestCase):
    def test_bootstrap_arithmetic(self):
        values = {"s": 0.2, "next": 0.6}
        result = update_value(values, "s", 0, "next", False, 0.1)
        self.assertAlmostEqual(result["target"], 0.6)
        self.assertAlmostEqual(result["td_error"], 0.4)
        self.assertAlmostEqual(values["s"], 0.24)
        self.assertEqual(values["next"], 0.6)

    def test_terminal_ignores_even_same_observation_value(self):
        # Standing may return the same player observation; it is nevertheless terminal.
        for reward in (-1, 0, 1):
            values = {"s": 0.8}
            result = update_value(values, "s", reward, "s", True, 0.5)
            self.assertEqual(result["target"], reward)
            self.assertAlmostEqual(values["s"], 0.8 + 0.5 * (reward - 0.8))

    def test_learning_propagates_on_later_visits(self):
        values = {}
        update_value(values, "a", 0, "b", False, 0.5)
        update_value(values, "b", 1, "terminal", True, 0.5)
        self.assertEqual(values, {"a": 0, "b": 0.5})
        update_value(values, "a", 0, "b", False, 0.5)
        self.assertEqual(values["a"], 0.25)
        self.assertNotIn("terminal", values)

    def test_same_fixed_policy_produces_same_games_as_mc(self):
        td = estimate_values(500, 7)
        mc = monte_carlo(500, 7, 17)
        for key in ("wins", "losses", "pushes", "mean_return"):
            self.assertEqual(td[key], mc[key])
        self.assertEqual(td, estimate_values(500, 7))
        self.assertTrue(all(-1 <= row["value"] <= 1 for row in td["states"]))

    def test_trace_matches_online_updates(self):
        report = estimate_values(1, 7)
        values = {}
        for row in report["first_episode"]:
            before = copy.deepcopy(values)
            result = update_value(values, tuple(row["observation"]), row["reward"],
                                  tuple(row["next_observation"]), row["done"], 0.1)
            self.assertEqual(result["old_value"], before.get(tuple(row["observation"]), 0))
            for key, value in result.items():
                self.assertEqual(row[key], value)
        self.assertEqual(report["states"], [{"observation": list(s), "visits": 1,
                                          "value": values[s]} for s in sorted(values)])

    def test_invalid_settings(self):
        for alpha in (0, -0.1, 1.1, float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                estimate_values(1, 7, alpha=alpha)
        for episodes, threshold in ((0, 17), (1, 3), (1, 22)):
            with self.assertRaises(ValueError):
                estimate_values(episodes, 7, threshold)
