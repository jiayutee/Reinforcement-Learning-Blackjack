import copy
import random
import unittest
from unittest.mock import Mock

from foundations.blackjack import HIT, STAND
from foundations.monte_carlo import EpisodeStep
from foundations.control import epsilon_greedy, evaluate, experiment, greedy_action, train, update_action_values


class ControlTests(unittest.TestCase):
    def test_action_values_are_separate_first_visit_means(self):
        state = (16, 10, False)
        q, counts = {}, {}
        episode = [EpisodeStep(state, HIT, 1.0), EpisodeStep(state, STAND, 2.0), EpisodeStep(state, HIT, 3.0)]
        update_action_values(episode, q, counts)
        self.assertEqual(q, {(state, HIT): 6.0, (state, STAND): 5.0})
        self.assertEqual(counts, {(state, HIT): 1, (state, STAND): 1})
        update_action_values([EpisodeStep(state, HIT, -1.0)], q, counts)
        self.assertEqual(q[(state, HIT)], 2.5)
        self.assertEqual(q[(state, STAND)], 5.0)

    def test_greedy_chooses_better_action_and_stands_on_ties(self):
        state = (16, 10, False)
        self.assertEqual(greedy_action(state, {}), STAND)
        self.assertEqual(greedy_action(state, {(state, HIT): -0.4, (state, STAND): -0.6}), HIT)
        self.assertEqual(greedy_action(state, {(state, HIT): 0.2, (state, STAND): 0.2}), STAND)

    def test_exploration_can_choose_either_action_including_greedy(self):
        state = (20, 10, False)
        q = {(state, STAND): 1.0, (state, HIT): -1.0}
        for action in (STAND, HIT):
            rng = Mock()
            rng.random.return_value = 0.01
            rng.choice.return_value = action
            self.assertEqual(epsilon_greedy(state, q, rng, 0.1), action)
            rng.choice.assert_called_once_with((STAND, HIT))

    def test_no_exploration_selects_only_maximizing_action(self):
        state = (16, 10, False)
        q = {(state, STAND): -0.8, (state, HIT): -0.3}
        self.assertEqual(epsilon_greedy(state, q, random.Random(7), 0), HIT)

    def test_evaluation_does_not_mutate_q_or_learn_unseen_states(self):
        q, counts, _ = train(100, 7, 0.1)
        before = copy.deepcopy(q)
        result = evaluate(q, 100, 100007)
        self.assertEqual(q, before)
        self.assertEqual(result['wins'] + result['losses'] + result['pushes'], 100)
        empty = {}
        result = evaluate(empty, 50, 42)
        self.assertEqual(empty, {})
        self.assertEqual(result['unvisited_selected_actions'], result['decisions'])

    def test_training_is_reproducible(self):
        self.assertEqual(train(200, 7, 0.1), train(200, 7, 0.1))

    def test_invalid_parameters_are_rejected(self):
        for epsilon in (-0.1, 1.1, float('nan')):
            with self.assertRaises(ValueError):
                train(10, 7, epsilon)
        with self.assertRaises(ValueError):
            train(0, 7, 0.1)
        with self.assertRaises(ValueError):
            evaluate({}, 1, 7)
        with self.assertRaises(ValueError):
            experiment(100, 100, 7, 7, 0.1)


if __name__ == '__main__':
    unittest.main()
