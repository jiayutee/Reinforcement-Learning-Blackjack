import unittest
from unittest.mock import patch

from foundations.blackjack import Blackjack, HIT, STAND, score_hand


class FoundationsTests(unittest.TestCase):
    def test_aces(self):
        for cards, expected in [([1, 6], (17, True)), ([1, 1, 9], (21, True)),
                                ([1, 6, 10], (17, False)), ([1, 1, 10], (12, False)),
                                ([10, 10, 5], (25, False))]:
            with self.subTest(cards=cards):
                self.assertEqual(score_hand(cards), expected)

    def play_script(self, cards, actions):
        env = Blackjack()
        with patch.object(env, "_draw", side_effect=cards) as draw:
            observation = env.reset()
            transitions = [env.step(action) for action in actions]
            return observation, transitions, draw.call_count

    def test_dealer_stands_on_soft_seventeen(self):
        _, steps, draws = self.play_script([10, 8, 1, 6], [STAND])
        self.assertEqual(steps[-1][1:], (1.0, True))
        self.assertEqual(draws, 4)

    def test_player_bust_does_not_play_dealer(self):
        _, steps, draws = self.play_script([10, 8, 5, 6, 10], [HIT])
        self.assertEqual(steps[-1], ((28, 5, False), -1.0, True))
        self.assertEqual(draws, 5)

    def test_hit_then_dealer_bust(self):
        _, steps, _ = self.play_script([5, 6, 10, 6, 8, 10], [HIT, STAND])
        self.assertEqual(steps[0], ((19, 10, False), 0.0, False))
        self.assertEqual(steps[1][1:], (1.0, True))

    def test_simplified_natural_pushes_against_three_card_twenty_one(self):
        _, steps, _ = self.play_script([1, 10, 5, 6, 10], [STAND])
        self.assertEqual(steps[-1][1:], (0.0, True))

    def test_natural_has_no_bonus(self):
        _, steps, _ = self.play_script([1, 10, 10, 8], [STAND])
        self.assertEqual(steps[-1][1:], (1.0, True))

    def test_lower_total_loses(self):
        _, steps, _ = self.play_script([10, 7, 10, 8], [STAND])
        self.assertEqual(steps[-1][1:], (-1.0, True))

    def test_hidden_card_is_not_in_observation(self):
        first, _, _ = self.play_script([10, 8, 10, 7], [STAND])
        second, _, _ = self.play_script([10, 8, 10, 9], [STAND])
        self.assertEqual(first, second)
        self.assertEqual(first, (18, 10, False))

    def test_invalid_and_terminal_actions(self):
        env = Blackjack()
        with self.assertRaises(RuntimeError):
            env.step(HIT)
        env.reset()
        for action in (-1, 2, "hit", True, 1.0):
            with self.assertRaises(ValueError):
                env.step(action)
        env.step(STAND)
        with self.assertRaises(RuntimeError):
            env.step(HIT)
        env.reset()
        env.step(STAND)

    def test_seed_reproduces_multiple_episodes(self):
        left, right = Blackjack(42), Blackjack(42)
        for _ in range(100):
            self.assertEqual(left.reset(), right.reset())
            done = False
            while not done:
                action = HIT if left._observation()[0] < 17 else STAND
                transition = left.step(action)
                self.assertEqual(transition, right.step(action))
                done = transition[2]


if __name__ == "__main__":
    unittest.main()
