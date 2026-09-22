import importlib.util
import unittest

from foundations.check_reference import check_hand_scores, check_scripted_transitions


@unittest.skipUnless(importlib.util.find_spec("gymnasium"), "optional Gymnasium reference is not installed")
class ReferenceChecks(unittest.TestCase):
    def test_rank_probabilities_and_hand_scoring_match(self):
        self.assertEqual(check_hand_scores(), 8007)

    def test_legal_scripted_transitions_match(self):
        self.assertEqual(check_scripted_transitions(), {"cases": 10, "transitions": 13})


if __name__ == "__main__":
    unittest.main()
