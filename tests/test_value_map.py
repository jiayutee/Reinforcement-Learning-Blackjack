import copy
import json
import re
import unittest

from foundations.monte_carlo import estimate_values
from foundations.value_map import render_report


class ValueMapTests(unittest.TestCase):
    def setUp(self):
        self.report = estimate_values(10, 7, 17)

    def test_embedded_data_preserves_estimates_and_unknowns(self):
        html = render_report(self.report)
        payload = re.search(r'<script id="report" type="application/json">(.*?)</script>', html, re.S).group(1)
        self.assertEqual(json.loads(payload), self.report)
        self.assertNotIn('"visits": 0', payload)

    def test_metadata_cannot_close_data_script(self):
        self.report['source'] = {'note': '</script><script>alert(1)</script>'}
        html = render_report(self.report)
        self.assertNotIn('</script><script>alert(1)', html)
        payload = re.search(r'<script id="report" type="application/json">(.*?)</script>', html, re.S).group(1)
        self.assertEqual(json.loads(payload)['source'], self.report['source'])

    def test_rejects_incompatible_rules(self):
        self.report['rules'] = 'six-deck casino rules'
        with self.assertRaises(ValueError):
            render_report(self.report)

    def test_rejects_unreliable_or_ambiguous_rows(self):
        for field, bad in [('visits', 0), ('visits', 11), ('value', float('nan')), ('value', 1.5), ('observation', [26, 10, False])]:
            with self.subTest(field=field, bad=bad):
                report = copy.deepcopy(self.report)
                report['states'][0][field] = bad
                with self.assertRaises(ValueError):
                    render_report(report)
        self.report['states'].append(self.report['states'][0])
        with self.assertRaises(ValueError):
            render_report(self.report)

    def test_rejects_inconsistent_summary(self):
        self.report['mean_return'] = 123.0
        with self.assertRaises(ValueError):
            render_report(self.report)


if __name__ == '__main__':
    unittest.main()
