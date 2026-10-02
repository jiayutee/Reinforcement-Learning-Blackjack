import copy
import unittest
from foundations.policy import FrozenPolicy
from foundations.q_learning import experiment


class FrozenPolicyTests(unittest.TestCase):
    def setUp(self):
        self.report = experiment(5, 2, 7, 1007, 0.1, 0.1)
        self.report['training']['episodes'] = 100
        self.report['states'] = [{'observation': [20, 10, False], 'greedy_action': 0,
            'actions': [{'action': 0, 'value': 0.4, 'visits': 50},
                        {'action': 1, 'value': -0.8, 'visits': 5}]}]

    def test_decision_evidence_and_no_mutation(self):
        original = copy.deepcopy(self.report)
        policy = FrozenPolicy(self.report)
        first = policy.advise((20, 10, False))
        self.assertEqual(first['action'], 0)
        self.assertEqual(first['actions'][1]['visits'], 5)
        self.assertEqual(first['status'], 'estimated')
        self.assertEqual(self.report, original)
        self.report['states'][0]['actions'][0]['value'] = -1
        first['actions'][0]['value'] = 99
        self.assertEqual(policy.advise((20, 10, False))['actions'][0]['value'], 0.4)

    def test_absent_and_unvisited_withhold_advice(self):
        self.assertIsNone(FrozenPolicy(self.report).advise((12, 2, False))['action'])
        row = self.report['states'][0]
        row['actions'][1].update(value=None, visits=0)
        result = FrozenPolicy(self.report).advise((20, 10, False))
        self.assertEqual(result['status'], 'insufficient_evidence')
        self.assertIsNone(result['action'])
        self.assertIsNone(result['actions'][1]['value'])

    def test_rules_and_observation_validation(self):
        policy = FrozenPolicy(self.report)
        for observation in ((22, 10, False), (20, 0, False), (20, 10, 0), (True, 10, False)):
            with self.assertRaises(ValueError): policy.advise(observation)
        self.report['rules'] = 'six-deck'
        with self.assertRaises(ValueError): FrozenPolicy(self.report)

    def test_stand_tie_is_preserved(self):
        self.report['states'][0]['actions'][1]['value'] = 0.4
        self.assertEqual(FrozenPolicy(self.report).advise((20,10,False))['action'], 0)
