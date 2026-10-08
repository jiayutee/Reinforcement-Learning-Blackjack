import unittest
from unittest.mock import patch

from public_game.cards import Shoe, Card
from public_game.session import PublicSession


class PublicSessionTests(unittest.TestCase):
    def test_invalid_requests_preserve_state_and_future_draws(self):
        session, control = PublicSession(seed=7), PublicSession(seed=7)
        before = session.view()
        for stake, revision in [(20, True), (20, 1), (201, 0), (202, 0), (0, 0)]:
            with self.assertRaises(ValueError): session.deal(stake, revision)
            self.assertEqual(session.view(), before)
        self.assertEqual(session.deal(20, 0), control.deal(20, 0))

    def test_failed_draw_rolls_back_even_after_tentative_shuffle(self):
        session, control = PublicSession(seed=7), PublicSession(seed=7)
        for target in (session, control):
            for _ in range(212): target._state[0].draw()
        before = session.view()
        original_draw = Shoe.draw
        calls = []
        def fail_on_third(shoe):
            calls.append(1)
            if len(calls) == 3: raise RuntimeError('injected draw failure')
            return original_draw(shoe)
        with patch.object(Shoe, 'draw', fail_on_third):
            with self.assertRaises(RuntimeError): session.deal(20, 0)
        self.assertEqual(session.view(), before)
        self.assertEqual(session._state[0].remaining, 100)
        self.assertEqual(session.deal(20, 0), control.deal(20, 0))
        self.assertEqual(session._state[0]._rng.getstate(), control._state[0]._rng.getstate())
        self.assertEqual(session._state[0]._cards, control._state[0]._cards)

    def test_active_hand_conceals_hole_and_blocks_redeal(self):
        session = PublicSession()
        cards = [Card(r, 'hearts') for r in ('10', 'A', '7', '6')]
        with patch.object(Shoe, 'draw', side_effect=cards): view = session.deal(20, 0)
        self.assertEqual((view['phase'], view['balance'], view['revision']), ('player_turn', 180, 1))
        self.assertEqual(view['dealer'], [{'rank': 'A', 'suit': 'hearts'}, None])
        self.assertIsNone(view['dealer_total'])
        self.assertIsNone(view['profit'])
        before = session.view()
        view['player'][0]['rank'] = '2'
        self.assertEqual(session.view(), before)
        with self.assertRaises(ValueError): session.deal(20, 1)
        self.assertEqual(session.view(), before)

    def test_natural_credits_once_and_reveals(self):
        session = PublicSession()
        cards = [Card(r, 'hearts') for r in ('A', '10', 'K', '6')]
        with patch.object(Shoe, 'draw', side_effect=cards): view = session.deal(20, 0)
        self.assertEqual((view['balance'], view['profit'], view['phase']), (230, 30, 'settled'))
        self.assertEqual(view['dealer_total'], 16)
        self.assertIsNotNone(view['dealer'][1])
        for _ in range(3): self.assertEqual(session.view(), view)
        with self.assertRaises(ValueError): session.deal(20, 0)
        self.assertEqual(session.view(), view)
        with patch.object(Shoe, 'draw', side_effect=cards): again = session.deal(20, 1)
        self.assertEqual((again['balance'], again['revision']), (260, 2))

    def active(self, ranks):
        session = PublicSession()
        with patch.object(Shoe, 'draw', side_effect=[Card(r, 'hearts') for r in ranks]):
            session.deal(20, 0)
        return session

    def test_stand_soft17_push_and_dealer_draw(self):
        for ranks, extra, profit, total in [
            (('10','A','8','6'), [], 20, 17),
            (('10','10','8','8'), [], 0, 18),
            (('10','10','7','6'), ['3'], -20, 19),
            (('10','10','7','6'), ['K'], 20, 26),
        ]:
            with self.subTest(ranks=ranks, extra=extra):
                session = self.active(ranks)
                with patch.object(Shoe, 'draw', side_effect=[Card(r,'hearts') for r in extra]) as draw:
                    view = session.act('stand', 1)
                    self.assertEqual(draw.call_count, len(extra))
                self.assertEqual((view['phase'], view['revision']), ('settled', 2))
                self.assertEqual((view['profit'], view['balance']), (profit, 200+profit))
                self.assertEqual(view['dealer_total'], total)
                self.assertEqual(len(view['dealer']), 2+len(extra))
                with self.assertRaises(ValueError): session.act('stand', 2)
                self.assertEqual(session.view(), view)

    def test_hit_pending_21_and_bust(self):
        session = self.active(('5','10','6','7'))
        with patch.object(Shoe, 'draw', return_value=Card('2','clubs')):
            pending = session.act('hit', 1)
        self.assertEqual(pending['phase'], 'player_turn')
        self.assertIsNone(pending['dealer'][1])
        with patch.object(Shoe, 'draw', return_value=Card('8','clubs')) as draw:
            done = session.act('hit', 2)
            self.assertEqual(draw.call_count, 1)
        self.assertEqual((done['profit'], done['balance']), (20, 220))
        session = self.active(('10','2','9','3'))
        with patch.object(Shoe, 'draw', side_effect=[Card('K','clubs')]) as draw:
            bust = session.act('hit', 1)
            self.assertEqual(draw.call_count, 1)
        self.assertEqual((bust['profit'], bust['dealer_total']), (-20, 5))

    def test_action_failure_and_rejections_preserve_private_state(self):
        session = self.active(('10','2','7','3'))
        before, bundle = session.view(), session._state
        for action, revision in [('split',1), ('hit',0), ('stand',True)]:
            with self.assertRaises(ValueError): session.act(action, revision)
            self.assertIs(session._state, bundle)
        with patch.object(Shoe, 'draw', side_effect=[Card('2','clubs'), RuntimeError('failure')]):
            with self.assertRaises(RuntimeError): session.act('stand', 1)
        self.assertIs(session._state, bundle)
        self.assertEqual(session.view(), before)
        with self.assertRaises(ValueError): PublicSession().act('hit', 0)

    def test_double_one_card_and_conservation(self):
        for ranks, drawn, profit in [
            (('5','10','6','7'), 'K', 40),
            (('5','10','6','7'), '6', 0),
            (('5','10','6','7'), '2', -40),
            (('10','2','9','3'), 'K', -40),
        ]:
            with self.subTest(ranks=ranks, drawn=drawn):
                session = self.active(ranks)
                with patch.object(Shoe, 'draw', side_effect=[Card(drawn,'clubs')]) as draw:
                    view = session.act('double', 1)
                    self.assertEqual(draw.call_count, 1)
                self.assertEqual((view['phase'],view['stake']), ('settled',40))
                self.assertEqual(len(view['player']), 3)
                self.assertEqual((view['profit'],view['balance']), (profit,200+profit))
                with self.assertRaises(ValueError): session.act('double', 2)

    def test_double_rejects_insufficient_funds_and_after_hit(self):
        session = PublicSession(balance=20)
        with patch.object(Shoe,'draw',side_effect=[Card(r,'hearts') for r in ('5','10','6','7')]):
            session.deal(20,0)
        before = session._state
        with patch.object(Shoe,'draw') as draw:
            with self.assertRaises(ValueError): session.act('double',1)
            draw.assert_not_called()
        self.assertIs(session._state,before)
        session = self.active(('5','10','6','7'))
        with patch.object(Shoe,'draw',return_value=Card('2','clubs')): session.act('hit',1)
        before = session._state
        with self.assertRaises(ValueError): session.act('double',2)
        self.assertIs(session._state,before)

    def test_double_failure_restores_additional_debit_and_cards(self):
        session = self.active(('5','2','6','3'))
        before = session._state
        with patch.object(Shoe,'draw',side_effect=[Card('K','clubs'), RuntimeError('dealer failure')]):
            with self.assertRaises(RuntimeError): session.act('double',1)
        self.assertIs(session._state,before)
        self.assertEqual(session.view()['balance'],180)
