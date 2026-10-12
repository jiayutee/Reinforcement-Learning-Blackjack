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
