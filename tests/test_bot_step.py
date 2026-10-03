import unittest
from foundations.local_game import apply_table_command
from foundations.policy import FrozenPolicy
from foundations.session import GameSession


def fixture():
    return FrozenPolicy({'schema_version': 1, 'artifact_type': 'q_learning_control',
        'rules': 'foundations-v1: replacement draws, S17, no natural bonus, hit/stand',
        'gamma': 1, 'training': {'episodes': 100, 'environment_seed': 7, 'epsilon': 0.1, 'alpha': 0.1},
        'states': [{'observation': [9, 7, False], 'greedy_action': 1,
                    'actions': [{'action': 0, 'value': -0.4, 'visits': 10},
                                {'action': 1, 'value': 0.2, 'visits': 20}]}]})


class BotStepTests(unittest.TestCase):
    def test_one_bot_action_matches_manual_and_keeps_policy_frozen(self):
        policy = fixture()
        session, manual = GameSession(7), GameSession(7)
        session.command('deal', 0); manual.command('deal', 0)
        before = policy.advise((9, 7, False))
        result = apply_table_command(session, policy, 'bot', 1)
        manual.command('hit', 1)
        self.assertEqual(session.view(), manual.view())
        self.assertEqual(result['revision'], 2)
        self.assertEqual(len(result['hand']['player_cards']), 3)
        self.assertEqual(result['hand']['dealer_cards'], [7, None])
        self.assertEqual(policy.advise((9, 7, False)), before)
        self.assertIsNone(result['advice']['action'])

    def test_stale_missing_and_terminal_do_not_mutate(self):
        policy, session = fixture(), GameSession(7)
        with self.assertRaises(ValueError): apply_table_command(session, policy, 'bot', 0)
        session.command('deal', 0)
        before = session.view()
        for revision in (0, True, '1'):
            with self.assertRaises(ValueError): apply_table_command(session, policy, 'bot', revision)
        with self.assertRaises(ValueError): apply_table_command(session, None, 'bot', 1)
        self.assertEqual(session.view(), before)
        apply_table_command(session, policy, 'bot', 1)
        after = session.view()
        for revision in (1, 2):
            with self.assertRaises(ValueError): apply_table_command(session, policy, 'bot', revision)
        self.assertEqual(session.view(), after)
        session.command('stand', 2)
        terminal = session.view()
        with self.assertRaises(ValueError): apply_table_command(session, policy, 'bot', 3)
        self.assertEqual(session.view(), terminal)

    def test_manual_commands_still_work_without_policy(self):
        session = GameSession(7)
        self.assertEqual(apply_table_command(session, None, 'deal', 0)['revision'], 1)
        self.assertTrue(apply_table_command(session, None, 'stand', 1)['hand']['done'])
