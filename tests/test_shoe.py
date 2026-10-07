from collections import Counter
import unittest
from public_game.cards import Card, Shoe, RANKS, SUITS


class ShoeTests(unittest.TestCase):
    def test_six_deck_composition_and_exhaustion(self):
        shoe = Shoe()
        cards = [shoe.draw() for _ in range(312)]
        self.assertEqual(Counter(cards), Counter({Card(r, s): 6 for r in RANKS for s in SUITS}))
        self.assertEqual(Counter(c.rank for c in cards), Counter({r: 24 for r in RANKS}))
        self.assertEqual(sum(c.value == 10 for c in cards), 96)
        self.assertEqual(shoe.remaining, 0)
        with self.assertRaises(RuntimeError): shoe.draw()

    def test_single_deck_has_four_of_each_rank(self):
        shoe = Shoe(decks=1)
        cards = [shoe.draw() for _ in range(52)]
        self.assertEqual(len(set(cards)), 52)
        self.assertEqual(Counter(c.rank for c in cards), Counter({r: 4 for r in RANKS}))

    def test_cut_threshold_does_not_shuffle_on_draw(self):
        shoe = Shoe(decks=1, penetration=0.5)
        for _ in range(25): shoe.draw()
        self.assertFalse(shoe.needs_shuffle)
        self.assertFalse(shoe.prepare_round())
        shoe.draw()
        self.assertTrue(shoe.needs_shuffle)
        shoe.draw()
        self.assertEqual(shoe.remaining, 25)
        self.assertTrue(shoe.prepare_round())
        self.assertEqual(shoe.remaining, 52)
        self.assertFalse(shoe.needs_shuffle)

    def test_reproducible_shuffle_stream(self):
        first, second = Shoe(seed=7), Shoe(seed=7)
        for _ in range(234): self.assertEqual(first.draw(), second.draw())
        self.assertTrue(first.prepare_round()); self.assertTrue(second.prepare_round())
        self.assertEqual([first.draw() for _ in range(20)], [second.draw() for _ in range(20)])

    def test_values_and_validation(self):
        self.assertEqual(Card('A', 'spades').value, 1)
        self.assertEqual(Card('K', 'hearts').value, 10)
        self.assertEqual(Card('9', 'clubs').value, 9)
        for kwargs in ({'decks': True}, {'decks': 0}, {'decks': 9}, {'penetration': 0}, {'penetration': 1}, {'penetration': float('nan')}):
            with self.assertRaises(ValueError): Shoe(**kwargs)
        with self.assertRaises(ValueError): Card('11', 'spades')
        with self.assertRaises(ValueError): Card('A', 'stars')

    def test_public_round_reserve_boundary(self):
        from public_game.cards import PUBLIC_ROUND_RESERVE
        self.assertEqual(PUBLIC_ROUND_RESERVE, 101)
        shoe = Shoe(decks=6, penetration=0.75)
        for _ in range(211): shoe.draw()
        self.assertEqual(shoe.remaining, 101)
        self.assertFalse(shoe.prepare_round(PUBLIC_ROUND_RESERVE))
        shoe.draw()
        self.assertFalse(shoe.needs_shuffle)
        self.assertTrue(shoe.prepare_round(PUBLIC_ROUND_RESERVE))
        self.assertEqual(shoe.remaining, 312)

    def test_invalid_reserve_does_not_mutate_shoe(self):
        first, reference = Shoe(seed=7), Shoe(seed=7)
        for minimum in (-1, 313, True, 1.5):
            with self.assertRaises(ValueError): first.prepare_round(minimum)
        self.assertEqual([first.draw() for _ in range(20)], [reference.draw() for _ in range(20)])
        with self.assertRaises(ValueError): Shoe(decks=1).prepare_round(101)
