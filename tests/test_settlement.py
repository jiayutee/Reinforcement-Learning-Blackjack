import unittest
from public_game.cards import Card
from public_game.settlement import settle_hand


def cards(*ranks): return [Card(r, 'hearts') for r in ranks]


class SettlementTests(unittest.TestCase):
    def test_natural_and_equal_naturals(self):
        result = settle_hand(cards('A','K'), cards('10','9'), 20)
        self.assertEqual((result.outcome,result.credit,result.profit), ('natural',50,30))
        tied = settle_hand(cards('A','K'), cards('A','Q'),20)
        self.assertEqual((tied.outcome,tied.credit,tied.profit), ('push',20,0))

    def test_split_and_multicard_21_are_ordinary(self):
        for hand, split in ((cards('A','K'),True),(cards('7','7','7'),False)):
            win = settle_hand(hand,cards('10','9'),20,from_split=split)
            self.assertEqual((win.outcome,win.credit,win.profit),('win',40,20))
            loss = settle_hand(hand,cards('A','Q'),20,from_split=split)
            self.assertEqual(loss.profit,-20)

    def test_bust_push_loss_and_dealer_bust(self):
        cases=[(cards('K','Q','2'),cards('10','6'),-20),
               (cards('10','7'),cards('10','7'),0),
               (cards('10','7'),cards('10','8'),-20),
               (cards('10','7'),cards('10','8','9'),20)]
        for player,dealer,profit in cases:
            result=settle_hand(player,dealer,20)
            self.assertEqual(result.profit,profit)
            self.assertEqual(result.credit-result.stake,profit)

    def test_split_double_accounting_and_nonmutation(self):
        player,dealer=cards('10','9'),cards('10','8')
        before=(list(player),list(dealer))
        first=settle_hand(player,dealer,40,from_split=True)
        second=settle_hand(cards('10','7'),dealer,20,from_split=True)
        self.assertEqual(first.profit+second.profit,20)
        self.assertEqual(first.credit+second.credit,80)
        self.assertEqual(200-60+80-200,first.profit+second.profit)
        self.assertEqual((player,dealer),before)
        self.assertEqual(settle_hand(player,dealer,40,from_split=True),first)

    def test_incomplete_dealer_and_bad_stake_rejected(self):
        for stake in (0,-2,3,True,2.0):
            with self.assertRaises(ValueError): settle_hand(cards('10','7'),cards('10','8'),stake)
        with self.assertRaises(ValueError): settle_hand(cards('10','7'),cards('10','6'),20)
        with self.assertRaises(ValueError): settle_hand(cards('A'),cards('10','8'),20)
