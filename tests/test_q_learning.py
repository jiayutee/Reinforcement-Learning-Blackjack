import unittest
from unittest.mock import patch
from foundations.q_learning import update, train, experiment
from foundations.sarsa import update as sarsa_update


class TestQLearning(unittest.TestCase):
    def test_max_target_differs_from_exploratory_sarsa(self):
        q = {('s', 1): 0.2, ('next', 0): 0.8, ('next', 1): -0.4}
        other = dict(q)
        result = update(q, 's', 1, 0, 'next', False, 0.1)
        sarsa_update(other, 's', 1, 0, 'next', 1, False, 0.1)
        self.assertEqual(result['target'], 0.8)
        self.assertAlmostEqual(q[('s', 1)], 0.26)
        self.assertAlmostEqual(other[('s', 1)], 0.14)

    def test_terminal_masks_values_even_for_same_state(self):
        for reward in (-1, 0, 1):
            q = {('s', 0): 0.8, ('s', 1): 99}
            result = update(q, 's', 0, reward, 's', True, 0.5)
            self.assertEqual(result['target'], reward)
            self.assertAlmostEqual(q[('s', 0)], 0.8+0.5*(reward-0.8))

    def test_missing_action_uses_zero_initialization(self):
        q = {('next', 0): -0.5}
        self.assertEqual(update(q, 's', 1, 0, 'next', False, 0.1)['target'], 0)

    def test_behavior_explores_and_never_acts_after_terminal(self):
        class Scripted:
            def __init__(self, seed): self.count = 0
            def reset(self): return (12, 6, False)
            def step(self, action):
                self.count += 1
                if self.count == 1:
                    assert action == 1
                    return (18, 6, False), 0, False
                assert action == 0
                return (18, 6, False), 1, True
        with patch('foundations.q_learning.Blackjack', Scripted), patch(
                'foundations.q_learning.epsilon_greedy', side_effect=[1, 0]) as choose:
            q, counts, outcomes, trace = train(1, 7)
        self.assertEqual(choose.call_count, 2)
        self.assertEqual(sum(counts.values()), 2)
        self.assertEqual(q[((18, 6, False), 0)], 0.1)

    def test_repeatability_and_validation(self):
        self.assertEqual(train(500, 7), train(500, 7))
        for kwargs in ({'alpha': 0}, {'alpha': float('nan')}, {'epsilon': 2}):
            with self.assertRaises(ValueError): train(1, 7, **kwargs)
        with self.assertRaises(ValueError): train(0, 7)
        with self.assertRaises(ValueError): experiment(1, 2, 7, 7, 0.1, 0.1)
        with self.assertRaises(ValueError): experiment(1, 1, 7, 8, 0.1, 0.1)
