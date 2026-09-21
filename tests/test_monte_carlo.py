import unittest
from unittest.mock import patch

from foundations.blackjack import Blackjack, HIT, STAND
from foundations.monte_carlo import (
    EpisodeStep, estimate_values, record_episode, returns_from_episode, update_first_visit,
)


class MonteCarloTests(unittest.TestCase):
    def test_returns_include_only_current_and_future_rewards(self):
        # Artificial rewards make accidental whole-episode/last-visit updates visible.
        episode = [EpisodeStep((10, 2, False), HIT, 2.0),
                   EpisodeStep((15, 2, False), HIT, -1.0),
                   EpisodeStep((20, 2, False), STAND, 3.0)]
        self.assertEqual(returns_from_episode(episode), [4.0, 2.0, 3.0])

    def test_incremental_average_matches_hand_calculation(self):
        state = (20, 10, False)
        values, counts = {}, {}
        for reward, expected in [(1.0, 1.0), (-1.0, 0.0), (1.0, 1.0 / 3.0)]:
            update_first_visit([EpisodeStep(state, STAND, reward)], values, counts)
            self.assertAlmostEqual(values[state], expected)
        self.assertEqual(counts[state], 3)

    def test_repeated_state_uses_first_occurrence_once(self):
        # Repeated observations need not occur in this blackjack profile; the
        # estimator still needs the stated first-visit semantics for later tasks.
        a, b = (10, 2, False), (15, 2, False)
        episode = [EpisodeStep(a, HIT, 1.0), EpisodeStep(b, HIT, 2.0),
                   EpisodeStep(a, STAND, 3.0)]
        values, counts = {}, {}
        update_first_visit(episode, values, counts)
        self.assertEqual(values, {a: 6.0, b: 5.0})
        self.assertEqual(counts, {a: 1, b: 1})
        update_first_visit([EpisodeStep(a, STAND, 0.0)], values, counts)
        self.assertEqual(values[a], 3.0)
        self.assertEqual(counts[a], 2)

    def test_push_counts_as_a_sample_and_unvisited_is_absent(self):
        values, counts = {}, {}
        state = (18, 10, False)
        update_first_visit([EpisodeStep(state, STAND, 0.0)], values, counts)
        self.assertEqual(values[state], 0.0)
        self.assertEqual(counts[state], 1)
        self.assertNotIn((19, 10, False), values)

    def test_recorded_hand_credits_decisions_not_terminal_observation(self):
        env = Blackjack()
        with patch.object(env, "_draw", side_effect=[5, 6, 10, 6, 10, 10]):
            episode = record_episode(env, threshold=17)
        self.assertEqual(episode, [EpisodeStep((11, 10, False), HIT, 0.0),
                                   EpisodeStep((21, 10, False), STAND, 1.0)])
        self.assertEqual(returns_from_episode(episode), [1.0, 1.0])

    def test_bust_has_only_pre_action_state(self):
        env = Blackjack()
        with patch.object(env, "_draw", side_effect=[10, 6, 10, 7, 10]):
            episode = record_episode(env, threshold=17)
        self.assertEqual(episode, [EpisodeStep((16, 10, False), HIT, -1.0)])

    def test_prediction_preserves_existing_threshold_baseline(self):
        report = estimate_values(10000, seed=7, threshold=17)
        self.assertEqual((report["wins"], report["losses"], report["pushes"]),
                         (4009, 4922, 1069))
        self.assertAlmostEqual(report["mean_return"], -0.0913)
        self.assertFalse(report["policy"]["learned"])
        for row in report["states"]:
            self.assertGreater(row["visits"], 0)
            self.assertLessEqual(row["visits"], report["episodes"])
            self.assertLessEqual(abs(row["value"]), 1.0)
            self.assertLessEqual(row["observation"][0], 21)

    def test_reproducible_estimates(self):
        self.assertEqual(estimate_values(100, 42, 18), estimate_values(100, 42, 18))

    def test_invalid_experiment_parameters(self):
        for episodes, threshold in [(0, 17), (-1, 17), (10, 3), (10, 22)]:
            with self.assertRaises(ValueError):
                estimate_values(episodes, 7, threshold)


if __name__ == "__main__":
    unittest.main()
