import unittest
from foundations.local_game import table_view
from foundations.session import GameSession


class TableAdviceTests(unittest.TestCase):
    def test_only_visible_observation_and_no_session_mutation(self):
        class Recorder:
            def advise(self, observation):
                self.observation = observation
                return {'action': 1}
        session, policy = GameSession(7), Recorder()
        session.command('deal', 0)
        before = session.view()
        result = table_view(session, policy)
        self.assertEqual(policy.observation, (9, 7, False))
        self.assertEqual(result['hand']['dealer_cards'], [7, None])
        self.assertEqual(result['advice'], {'action': 1})
        self.assertEqual(session.view(), before)
        self.assertEqual(table_view(session, policy), result)

    def test_no_advice_before_deal_after_end_or_without_policy(self):
        class NeverCalled:
            def advise(self, observation): raise AssertionError('No active decision')
        session = GameSession(7)
        self.assertIsNone(table_view(session, NeverCalled())['advice'])
        session.command('deal', 0)
        self.assertFalse(table_view(session)['advisor_loaded'])
        self.assertIsNone(table_view(session)['advice'])
        session.command('stand', 1)
        self.assertIsNone(table_view(session, NeverCalled())['advice'])
