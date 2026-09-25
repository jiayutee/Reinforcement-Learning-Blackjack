import copy
import unittest

from foundations.control import experiment
from foundations.policy_table import cell, index_states, render_policy_table


class PolicyTableTests(unittest.TestCase):
    def setUp(self):
        self.report = experiment(5, 2, 7, 1007, 0.1)
        self.report['training']['episodes'] = 100
        self.report['states'] = [{'observation': [20, 10, False], 'greedy_action': 0,
                                 'actions': [{'action': 0, 'value': 0.4, 'visits': 50},
                                             {'action': 1, 'value': -0.8, 'visits': 5}]}]

    def test_warns_on_rare_alternative_not_only_selected_action(self):
        row = index_states(self.report)[(20, 10, False)]
        self.assertEqual(cell(row, 20), 'S*')
        self.assertEqual(cell(row, 5), 'S')
        self.assertEqual(cell(None, 20), '—')

    def test_untried_is_unknown_not_a_zero_value(self):
        self.report['states'][0]['actions'][1].update(value=None, visits=0)
        rendered = render_policy_table(self.report)
        self.assertIn('unknown / 0', rendered)
        self.assertEqual(cell(index_states(self.report)[(20,10,False)], 20), '?')

    def test_rendering_preserves_input_and_keeps_numeric_evidence(self):
        before = copy.deepcopy(self.report)
        text = render_policy_table(self.report)
        self.assertIn('+0.40000 / 50', text)
        self.assertIn('-0.80000 / 5', text)
        self.assertEqual(self.report, before)

    def test_unknown_source_cleanliness_stays_unknown(self):
        self.report['source'] = {'git_commit': 'a' * 40, 'foundations_source_dirty': None}
        self.assertIn('Foundations source dirty: `unknown`', render_policy_table(self.report))

    def test_rejects_inconsistent_stored_decision(self):
        self.report['states'][0]['greedy_action'] = 1
        with self.assertRaises(ValueError):
            render_policy_table(self.report)

    def test_rejects_different_artifact_and_unvisited_fake_value(self):
        bad = copy.deepcopy(self.report)
        bad['artifact_type'] = 'state_values'
        with self.assertRaises(ValueError):
            render_policy_table(bad)
        self.report['states'][0]['actions'][1].update(value=0.0, visits=0)
        with self.assertRaises(ValueError):
            render_policy_table(self.report)


if __name__ == '__main__':
    unittest.main()
