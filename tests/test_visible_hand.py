import json
import unittest
from unittest.mock import patch
from foundations.blackjack import Blackjack, HIT, STAND


class VisibleHandTests(unittest.TestCase):
    def make_hand(self, cards):
        env = Blackjack(7)
        with patch.object(env, '_draw', side_effect=cards):
            env.reset()
        return env

    def test_before_reset_and_hidden_card_noninterference(self):
        with self.assertRaises(RuntimeError): Blackjack().visible_hand()
        first = self.make_hand([10, 7, 6, 1])
        second = self.make_hand([10, 7, 6, 10])
        self.assertEqual(first.visible_hand(), second.visible_hand())
        view = first.visible_hand()
        self.assertEqual(view['dealer_cards'], [6, None])
        self.assertIsNone(view['dealer_total'])
        self.assertEqual(view['legal_actions'], [STAND, HIT])
        self.assertEqual(json.loads(json.dumps(view)), view)

    def test_nonterminal_hit_keeps_dealer_hidden(self):
        env = self.make_hand([2, 3, 6, 10])
        with patch.object(env, '_draw', return_value=4): env.step(HIT)
        view = env.visible_hand()
        self.assertEqual(view['player_cards'], [2, 3, 4])
        self.assertEqual(view['player_total'], 9)
        self.assertEqual(view['dealer_cards'], [6, None])
        self.assertFalse(view['done'])

    def test_stand_and_bust_reveal_but_disable_actions(self):
        env = self.make_hand([10, 7, 10, 7])
        env.step(STAND)
        self.assertEqual(env.visible_hand()['dealer_cards'], [10, 7])
        self.assertEqual(env.visible_hand()['dealer_total'], 17)
        self.assertEqual(env.visible_hand()['legal_actions'], [])
        env = self.make_hand([10, 9, 6, 10])
        with patch.object(env, '_draw', return_value=5): env.step(HIT)
        self.assertTrue(env.visible_hand()['done'])
        self.assertEqual(env.visible_hand()['dealer_cards'], [6, 10])
        self.assertEqual(env.visible_hand()['legal_actions'], [])

    def test_view_mutation_and_reads_do_not_change_game(self):
        env, reference = Blackjack(7), Blackjack(7)
        self.assertEqual(env.reset(), reference.reset())
        view = env.visible_hand()
        view['player_cards'].clear()
        view['dealer_cards'][0] = 99
        view['legal_actions'].clear()
        for _ in range(3): env.visible_hand()
        self.assertEqual(env.step(STAND), reference.step(STAND))
        self.assertEqual(env.visible_hand(), reference.visible_hand())
        self.assertEqual(env.reset(), reference.reset())
        self.assertEqual(env.visible_hand()['dealer_cards'][1], None)
