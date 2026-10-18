import unittest

from public_game.experiment import run_prediction


class PublicMonteCarloExperimentTests(unittest.TestCase):
    def test_prediction_run_is_seeded_and_reports_visit_counts(self):
        first = run_prediction(episodes=80, seed=11)
        second = run_prediction(episodes=80, seed=11)
        self.assertEqual(first, second)
        self.assertEqual(first['episodes'], 80)
        self.assertEqual(first['decision_episodes'] + first['opening_naturals'], 80)
        self.assertGreater(first['estimated_states'], 0)
        self.assertEqual(first['reported_states'], len(first['estimates']))
        self.assertGreaterEqual(first['estimated_states'], first['reported_states'])
        self.assertLessEqual(first['reported_states'], 12)
        for estimate in first['estimates']:
            self.assertGreater(estimate['count'], 0)
            self.assertLessEqual(estimate['count'], first['decision_episodes'])
            # Four doubled split hands can move normalized profit outside ±1.
            self.assertTrue(-8 <= estimate['value'] <= 8)

    def test_prediction_rejects_nonpositive_episode_count_and_bad_top(self):
        for episodes in (0, -1, True):
            with self.assertRaises(ValueError):
                run_prediction(episodes=episodes, seed=1)
        for top in (-1, True):
            with self.assertRaises(ValueError):
                run_prediction(episodes=1, seed=1, top=top)


if __name__ == '__main__':
    unittest.main()
