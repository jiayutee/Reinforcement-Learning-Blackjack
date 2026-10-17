import unittest
from public_game.experiment import run_experiment, threshold_policy


class ExperimentTests(unittest.TestCase):
    def test_reproducible_fixed_policy(self):
        first = run_experiment(100, 17)
        self.assertEqual(first, run_experiment(100, 17))
        self.assertEqual(first['wins'] + first['losses'] + first['pushes'], 100)
        self.assertGreater(first['decision_transitions'], 0)
        self.assertIn('ignores soft/pair', first['policy'])

    def test_policy_uses_only_hand_total(self):
        view = {'active_hand': 0, 'hands': [{'total': 16}]}
        self.assertEqual(threshold_policy(view), 'hit')
        view['hands'][0]['total'] = 17
        self.assertEqual(threshold_policy(view), 'stand')

    def test_invalid_trial_count(self):
        for value in (0, -1, True, 1.0):
            with self.assertRaises(ValueError): run_experiment(value, 1)
