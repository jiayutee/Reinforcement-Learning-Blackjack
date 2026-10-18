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

    def test_first_visit_mc_averages_returns_not_rewards(self):
        from dataclasses import dataclass
        from public_game.monte_carlo import FirstVisitMonteCarlo
        @dataclass
        class T:
            observation: dict
            reward: float
        @dataclass
        class E:
            transitions: tuple
            opening_terminal: bool = False
        state={'active_hand':0,'hands':[{'total':16,'usable_ace':False,'from_split':False,'split_aces':False}],
               'dealer':[{'rank':'10','suit':'clubs'},None], 'legal_actions':['hit','stand']}
        other={**state,'hands':[{'total':18,'usable_ace':False,'from_split':False,'split_aces':False}]}
        learner=FirstVisitMonteCarlo(gamma=1)
        learner.update(E((T(state,0),T(other,1))))
        self.assertEqual(learner.estimates[learner_key(state)].value,1)
        self.assertEqual(learner.estimates[learner_key(other)].value,1)
        learner.update(E((T(state,0),T(other,-1))))
        self.assertEqual(learner.estimates[learner_key(state)].value,0)
        self.assertEqual(learner.estimates[learner_key(state)].count,2)
        # The second state's returns are +1 then -1, also averaging to zero.
        self.assertEqual(learner.estimates[learner_key(other)].value,0)

    def test_first_visit_duplicate_state_updates_once_per_episode(self):
        from dataclasses import dataclass
        from public_game.monte_carlo import FirstVisitMonteCarlo, state_key
        @dataclass
        class T:
            observation: dict
            reward: float
        @dataclass
        class E:
            transitions: tuple
            opening_terminal: bool = False
        state={'active_hand':0,'hands':[{'total':10,'usable_ace':False,'from_split':False,'split_aces':False}],
               'dealer':[{'rank':'6'},None], 'legal_actions':['hit','stand']}
        learner=FirstVisitMonteCarlo()
        learner.update(E((T(state,0),T(state,1))))
        self.assertEqual(learner.estimates[state_key(state)].value,1)
        self.assertEqual(learner.estimates[state_key(state)].count,1)

    def test_discounted_returns_are_accumulated_backwards(self):
        from dataclasses import dataclass
        from public_game.monte_carlo import FirstVisitMonteCarlo, state_key
        @dataclass
        class T:
            observation: dict
            reward: float
        @dataclass
        class E:
            transitions: tuple
            opening_terminal: bool = False
        def observation(total):
            return {'active_hand':0,
                    'hands':[{'total':total,'usable_ace':False,'from_split':False,'split_aces':False}],
                    'dealer':[{'rank':'6'},None], 'legal_actions':['hit','stand']}
        states=[observation(total) for total in (10,11,12)]
        learner=FirstVisitMonteCarlo(gamma=0.5)
        learner.update(E(tuple(T(state,reward) for state,reward in zip(states,(0,0,1)))))
        self.assertEqual([learner.estimates[state_key(state)].value for state in states],
                         [0.25,0.5,1.0])

    def test_opening_natural_counted_separately_and_gamma_validated(self):
        from public_game.monte_carlo import FirstVisitMonteCarlo
        from public_game.episodes import Episode
        learner=FirstVisitMonteCarlo()
        learner.update(Episode((),1.5,True))
        self.assertEqual((learner.episodes,learner.decision_episodes,learner.opening_terminals),(1,0,1))
        for gamma in (-0.1,1.1,True):
            with self.assertRaises(ValueError): FirstVisitMonteCarlo(gamma)


def learner_key(observation):
    from public_game.monte_carlo import state_key
    return state_key(observation)
