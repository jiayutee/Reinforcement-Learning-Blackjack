import unittest
from unittest.mock import patch
from foundations.sarsa import update, train, experiment


class TestSARSA(unittest.TestCase):
    def test_target_uses_chosen_action_not_maximum(self):
        q = {('s', 1): 0.2, ('next', 0): 0.8, ('next', 1): -0.4}
        result = update(q, 's', 1, 0, 'next', 1, False, 0.1)
        self.assertEqual(result['target'], -0.4)
        self.assertAlmostEqual(q[('s', 1)], 0.14)
        self.assertEqual(q[('next', 0)], 0.8)

    def test_terminal_ignores_next_value(self):
        for reward in (-1, 0, 1):
            q = {('s', 0): 0.8, ('s', None): 99}
            result = update(q, 's', 0, reward, 's', None, True, 0.5)
            self.assertEqual(result['target'], reward)
            self.assertAlmostEqual(q[('s', 0)], 0.8 + 0.5 * (reward - 0.8))

    def test_selected_next_action_is_carried_forward(self):
        class Scripted:
            def __init__(self, seed): self.actions = []
            def reset(self): return (12, 6, False)
            def step(self, action):
                self.actions.append(action)
                if len(self.actions) == 1:
                    assert action == 1
                    return (18, 6, False), 0, False
                assert action == 0
                return (18, 6, False), 1, True
        with patch('foundations.sarsa.Blackjack', Scripted), patch(
                'foundations.sarsa.epsilon_greedy', side_effect=[1, 0]) as choose:
            q, counts, outcomes, trace = train(1, 7)
        self.assertEqual(choose.call_count, 2)
        self.assertEqual(trace[0]['next_action'], trace[1]['action'])
        self.assertIsNone(trace[-1]['next_action'])
        self.assertEqual(q[((12, 6, False), 1)], 0)
        self.assertEqual(q[((18, 6, False), 0)], 0.1)
        self.assertEqual(sum(counts.values()), 2)

    def test_reproducible_bounded_training(self):
        first = train(500, 7)
        self.assertEqual(first, train(500, 7))
        self.assertTrue(all(-1 <= value <= 1 for value in first[0].values()))
        self.assertEqual(sum(first[2][k] for k in ('wins', 'losses', 'pushes')), 500)

    def test_invalid_inputs(self):
        for setting in (0, -1, float('nan'), 1.1):
            with self.assertRaises(ValueError): train(1, 7, alpha=setting)
        for setting in (-0.1, float('inf'), 1.1):
            with self.assertRaises(ValueError): train(1, 7, epsilon=setting)
        with self.assertRaises(ValueError): train(0, 7)
        with self.assertRaises(ValueError): experiment(1, 2, 7, 7, 0.1, 0.1)
        with self.assertRaises(ValueError): experiment(1, 1, 7, 8, 0.1, 0.1)
