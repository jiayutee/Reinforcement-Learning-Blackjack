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
