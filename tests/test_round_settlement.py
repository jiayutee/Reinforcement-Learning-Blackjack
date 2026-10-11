import unittest
from public_game.cards import Card
from public_game.splitting import SplitHand
from public_game.round_settlement import settle_round


def cards(*ranks): return tuple(Card(r,'hearts') for r in ranks)
def hand(ranks, stake=20, complete=True):
    return SplitHand(cards(*ranks),stake,True,False,complete)


class RoundSettlementTests(unittest.TestCase):
    def test_mixed_double_results_conserve_balance(self):
        hands = [hand(('10','9'),40), hand(('10','7'))]
        result = settle_round(hands,cards('10','8'),20)
        self.assertEqual((result.stake,result.credit,result.profit),(60,80,20))
        self.assertEqual(200-result.stake+result.credit-200,result.profit)
        self.assertEqual(result.normalized_profit,1)
        self.assertEqual([r.outcome for r in result.hands],['win','loss'])
        self.assertEqual(settle_round(hands,cards('10','8'),20),result)

    def test_four_doubles_and_all_bust_without_dealer_draw(self):
        wins = settle_round([hand(('10','9'),40)]*4,cards('10','8'),20)
        self.assertEqual(wins.normalized_profit,8)
        busts = settle_round([hand(('10','9','K'),40)]*4,cards('2','3'),20)
        self.assertEqual((busts.credit,busts.normalized_profit),(0,-8))

    def test_incomplete_and_inconsistent_inputs_rejected(self):
        for hands in ([], [hand(('10','9'))]*5, [hand(('10','9'),complete=False)],
                      [hand(('10','9'),60)]):
            with self.assertRaises(ValueError): settle_round(hands,cards('10','8'),20)
        with self.assertRaises(ValueError): settle_round([hand(('10','9'))],cards('2','3'),20)
        for stake in (0,3,True):
            with self.assertRaises(ValueError): settle_round([hand(('10','9'))],cards('10','8'),stake)
