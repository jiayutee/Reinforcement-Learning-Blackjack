import unittest
from public_game.play import run, format_view
from public_game.session import PublicSession


class PublicPlayTests(unittest.TestCase):
    def test_scripted_round_and_bad_commands(self):
        session = PublicSession(seed=7)
        commands = iter(['deal nonsense','deal 10','deal 10','stand','quit'])
        output = []
        run(session, lambda prompt: next(commands), output.append)
        self.assertEqual(session.view()['revision'],2)
        self.assertEqual(sum(text.startswith('Rejected:') for text in output),2)
        self.assertIn('??',output[3])
        self.assertIn('Round profit: -10 chips | normalized: -1',output[-1])
        self.assertNotIn('??',output[-1])

    def test_eof_and_visible_only_formatting(self):
        session = PublicSession(seed=7)
        def eof(prompt): raise EOFError
        run(session,eof,lambda text: None)
        self.assertEqual(session.view()['revision'],0)
        view = session.deal(20,0)
        before = session.view()
        self.assertIn('??',format_view(view))
        self.assertEqual(session.view(),before)

    def test_split_double_display_follows_active_hand(self):
        from unittest.mock import patch
        from public_game.cards import Card, Shoe
        session = PublicSession()
        commands = iter(['deal 10','split','double','stand','quit'])
        output = []
        # Opening 8+8 vs18; split to11/17; double first to21.
        ranks = ('8','10','8','8','3','9','K')
        with patch.object(Shoe,'draw',side_effect=[Card(r,'hearts') for r in ranks]):
            run(session,lambda prompt: next(commands),output.append)
        split, doubled, settled = output[3:6]
        self.assertIn('Hand 1 ->:',split)
        self.assertIn('Hand 2:',split)
        self.assertIn('Hand 2 ->:',doubled)
        self.assertIn('stake 20 chips',doubled)
        self.assertIn('??',doubled)
        self.assertNotIn('Round profit:',doubled)
        self.assertNotIn('??',settled)
        self.assertNotIn(' ->:',settled)
        self.assertIn('Round profit: 10 chips | normalized: 1',settled)
        self.assertEqual(session.view()['balance'],220)

    def test_visible_totals_soft_to_hard_and_dealer_concealment(self):
        from unittest.mock import patch
        from public_game.cards import Card, Shoe
        session = PublicSession()
        with patch.object(Shoe,'draw',side_effect=[Card(r,'hearts') for r in ('A','10','6','8')]):
            view = session.deal(20,0)
        text = format_view(view)
        self.assertIn('soft 17',text)
        self.assertNotIn('total 18',text)
        with patch.object(Shoe,'draw',return_value=Card('K','clubs')):
            view = session.act('hit',1)
        self.assertIn('hard 17',format_view(view))
        view = session.act('stand',2)
        self.assertIn('total 18',format_view(view))
