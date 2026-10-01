import unittest
from foundations.session import GameSession


class SessionTests(unittest.TestCase):
    def test_lifecycle_and_reveal(self):
        session = GameSession(7)
        self.assertEqual(session.view(), {'revision': 0, 'hand': None, 'reward': None})
        dealt = session.command('deal', 0)
        self.assertEqual(dealt['hand']['dealer_cards'][1], None)
        self.assertIsNone(dealt['reward'])
        result = session.command('stand', 1)
        self.assertTrue(result['hand']['done'])
        self.assertIn(result['reward'], (-1, 0, 1))
        self.assertNotIn(None, result['hand']['dealer_cards'])
        again = session.command('deal', 2)
        self.assertEqual(again['revision'], 3)
        self.assertIsNone(again['reward'])
        self.assertFalse(again['hand']['done'])

    def test_rejected_commands_preserve_view_and_random_stream(self):
        session, reference = GameSession(7), GameSession(7)
        for name, revision in [('hit', 0), ('stand', 0), ('unknown', 0), ('deal', True), ('deal', -1)]:
            with self.assertRaises(ValueError): session.command(name, revision)
        self.assertEqual(session.command('deal', 0), reference.command('deal', 0))
        before = session.view()
        for name, revision in [('deal', 1), ('hit', 0), ('stand', '1')]:
            with self.assertRaises(ValueError): session.command(name, revision)
            self.assertEqual(session.view(), before)
        self.assertEqual(session.command('stand', 1), reference.command('stand', 1))
        with self.assertRaises(ValueError): session.command('hit', 2)
        self.assertEqual(session.command('deal', 2), reference.command('deal', 2))

    def test_duplicate_hit_applies_only_once(self):
        session = GameSession(7)
        session.command('deal', 0)
        result = session.command('hit', 1)
        self.assertFalse(result['hand']['done'])
        self.assertIsNone(result['reward'])
        self.assertEqual(len(result['hand']['player_cards']), 3)
        with self.assertRaises(ValueError): session.command('hit', 1)
        self.assertEqual(session.view(), result)

    def test_detached_views_and_session_isolation(self):
        first, second = GameSession(7), GameSession(7)
        first.command('deal', 0)
        view = first.view()
        view['hand']['player_cards'].clear()
        view['revision'] = 100
        self.assertEqual(first.view()['revision'], 1)
        self.assertEqual(len(first.view()['hand']['player_cards']), 2)
        self.assertEqual(second.view()['revision'], 0)
