import unittest
from public_game.cards import Card
from public_game.splitting import split_hand
from public_game.hands import hand_facts
from public_game.settlement import settle_hand


def cards(*ranks): return [Card(r,'hearts') for r in ranks]


class SplitTests(unittest.TestCase):
    def test_order_stakes_and_extra_debit(self):
        pair, added = cards('8','8'), cards('3','K')
        hands, balance = split_hand(pair,added,20,180,1)
        self.assertEqual(balance,160)
        self.assertEqual([[c.rank for c in h.cards] for h in hands],[['8','3'],['8','K']])
        self.assertEqual(sum(h.stake for h in hands),40)
        self.assertTrue(all(h.from_split and not h.complete for h in hands))
        pair.clear(); added.clear()
        self.assertEqual(len(hands[0].cards),2)

    def test_split_aces_stop_and_21_is_ordinary(self):
        hands, _ = split_hand(cards('A','A'),cards('K','A'),20,180,1)
        self.assertTrue(all(h.complete and h.split_aces for h in hands))
        self.assertFalse(hand_facts(hands[0].cards,from_split=True).natural)
        result = settle_hand(hands[0].cards,cards('10','9'),20,from_split=True)
        self.assertEqual(result.profit,20)
        with self.assertRaises(ValueError):
            split_hand(hands[1].cards,cards('2','3'),20,160,2,split_aces=True)

    def test_rank_limit_funds_and_invalid_inputs(self):
        for pair, stake, balance, count in [
            (cards('J','K'),20,180,1), (cards('8','8'),20,19,1),
            (cards('8','8'),20,180,4), (cards('8','8'),20,180,True),
            (cards('8','8'),3,180,1), (cards('8','8','8'),20,180,1)]:
            with self.assertRaises(ValueError): split_hand(pair,cards('2','3'),stake,balance,count)
        for additions in (cards('2'), [None,None]):
            with self.assertRaises(ValueError): split_hand(cards('8','8'),additions,20,180,1)
        hands, balance = split_hand(cards('8','8'),cards('8','2'),20,20,3)
        self.assertEqual(balance,0)
        self.assertTrue(hand_facts(hands[0].cards).equal_rank_pair)
