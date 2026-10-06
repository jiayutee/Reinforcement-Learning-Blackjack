import unittest
from public_game.cards import Card
from public_game.hands import hand_facts


def cards(*ranks):
    return [Card(rank, 'spades') for rank in ranks]


class PublicHandTests(unittest.TestCase):
    def test_multiple_aces_and_soft_to_hard(self):
        self.assertEqual((hand_facts(cards('A','A','9')).total, hand_facts(cards('A','A','9')).usable_ace), (21, True))
        self.assertEqual((hand_facts(cards('A','6','10')).total, hand_facts(cards('A','6','10')).usable_ace), (17, False))
        self.assertTrue(hand_facts(cards('10','9','5')).bust)

    def test_natural_requires_two_cards_and_unsplit_context(self):
        for rank in ('10','J','Q','K'):
            self.assertTrue(hand_facts(cards('A',rank)).natural)
            split = hand_facts(cards('A',rank), from_split=True)
            self.assertEqual(split.total, 21)
            self.assertFalse(split.natural)
        self.assertFalse(hand_facts(cards('7','7','7')).natural)

    def test_equal_value_is_not_equal_rank(self):
        self.assertFalse(hand_facts(cards('J','K')).equal_rank_pair)
        self.assertTrue(hand_facts(cards('Q','Q')).equal_rank_pair)
        self.assertTrue(hand_facts(cards('A','A')).equal_rank_pair)
        self.assertFalse(hand_facts(cards('2','2','2')).equal_rank_pair)

    def test_no_mutation_and_validation(self):
        hand = cards('A','6')
        before = list(hand)
        hand_facts(hand)
        self.assertEqual(hand,before)
        for invalid in ([], [1,10]):
            with self.assertRaises(ValueError): hand_facts(invalid)
        with self.assertRaises(ValueError): hand_facts(hand, from_split=1)
