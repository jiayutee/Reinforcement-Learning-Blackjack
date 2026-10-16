import unittest
from unittest.mock import patch
from public_game.cards import Card, Shoe
from public_game.session import PublicSession
from public_game.episodes import collect_round


class EpisodeTests(unittest.TestCase):
    def test_split_round_terminal_reward_once(self):
        actions=iter(['split','double','stand'])
        session=PublicSession()
        with patch.object(Shoe,'draw',side_effect=[Card(r,'hearts') for r in ('8','10','8','8','3','9','K')]):
            episode=collect_round(session,lambda view: next(actions))
        self.assertEqual([t.reward for t in episode.transitions],[0,0,1])
        self.assertEqual([t.done for t in episode.transitions],[False,False,True])
        self.assertEqual(episode.normalized_profit,1)
        self.assertTrue(all(t.observation['dealer'][1] is None for t in episode.transitions))
        self.assertEqual(sum(t.reward for t in episode.transitions),episode.normalized_profit)

    def test_natural_has_outcome_but_no_invented_action(self):
        with patch.object(Shoe,'draw',side_effect=[Card(r,'hearts') for r in ('A','10','K','6')]):
            episode=collect_round(PublicSession(),lambda view: self.fail('policy called on terminal opening'))
        self.assertEqual(episode.transitions,())
        self.assertTrue(episode.opening_terminal)
        self.assertEqual(episode.normalized_profit,1.5)

    def test_policy_mutation_cannot_change_recorded_observation(self):
        session=PublicSession(seed=7)
        def policy(view):
            view['balance']=999
            view['hands'].clear()
            return 'stand'
        episode=collect_round(session,policy)
        self.assertEqual(episode.transitions[0].observation['balance'],180)
        self.assertEqual(len(episode.transitions[0].observation['hands']),1)
        self.assertEqual(session.view()['balance'],180)
        episode.transitions[0].next_observation['balance']=999
        self.assertEqual(session.view()['balance'],180)

    def test_illegal_policy_does_not_apply_action(self):
        session=PublicSession(seed=7)
        with self.assertRaises(ValueError): collect_round(session,lambda view:'invented')
        self.assertEqual(session.view()['revision'],1)
        self.assertEqual(session.view()['balance'],180)
