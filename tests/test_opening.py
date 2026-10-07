import unittest
from dataclasses import FrozenInstanceError

from public_game.cards import Card
from public_game.opening import opening_round, validate_wager


def deal(*ranks):
    return [Card(rank, 'hearts') for rank in ranks]


class OpeningTests(unittest.TestCase):
    def test_ordinary_deal_order_and_debit(self):
        result = opening_round(deal('10', 'A', '7', '6'), 201, 20)
        self.assertEqual(result.phase, 'player_turn')
        self.assertEqual([card.rank for card in result.player], ['10', '7'])
        self.assertEqual([card.rank for card in result.dealer], ['A', '6'])
        self.assertEqual(result.balance, 181)
        self.assertIsNone(result.settlement)

    def test_naturals_settle_before_any_player_action(self):
        cases = [
            (('A', '10', 'K', '6'), 'natural', 230, 30),
            (('10', 'A', '7', 'K'), 'loss', 180, -20),
            (('A', 'A', 'Q', 'K'), 'push', 200, 0),
        ]
        for ranks, outcome, balance, profit in cases:
            with self.subTest(ranks=ranks):
                result = opening_round(deal(*ranks), 200, 20)
                self.assertEqual(result.phase, 'settled')
                self.assertEqual(result.balance, balance)
                self.assertEqual(result.settlement.outcome, outcome)
                self.assertEqual(result.settlement.profit, profit)
                self.assertEqual(result.balance - 200, profit)

    def test_whole_chip_wager_can_pay_half_chip_profit(self):
        result = opening_round(deal('A', '10', 'K', '6'), 2, 2)
        self.assertEqual(result.balance, 5)
        self.assertEqual(result.settlement.profit, 3)
        validate_wager(result.balance, 4)

    def test_invalid_funds_wagers_and_cards(self):
        for balance in (-1, True, 200.0):
            with self.assertRaises(ValueError): validate_wager(balance, 20)
        for stake in (0, -2, 3, True, 2.0, 202):
            with self.assertRaises(ValueError): validate_wager(200, stake)
        with self.assertRaises(ValueError): validate_wager(0, 2)
        for cards in ([], deal('A', 'K'), deal('A', 'K', '2', '3', '4'),
                      [Card('A', 'hearts'), 10, 2, 3]):
            with self.assertRaises(ValueError): opening_round(cards, 200, 20)

    def test_detached_immutable_repeatable_result(self):
        cards = deal('A', '10', 'K', '6')
        before = list(cards)
        first = opening_round(cards, 200, 20)
        self.assertEqual(opening_round(cards, 200, 20), first)
        self.assertEqual(cards, before)
        cards.clear()
        self.assertEqual(len(first.player), 2)
        with self.assertRaises(FrozenInstanceError): first.balance = 999
        with self.assertRaises(FrozenInstanceError): first.player[0].rank = '2'
