"""Read-only decisions from a validated Foundations control export."""
import argparse
import json
from pathlib import Path

from foundations.policy_table import index_states


class FrozenPolicy:
    def __init__(self, report):
        # Reuse the control-artifact/rules/count/value checks used by the viewer.
        rows = index_states(report)
        self.algorithm = report['artifact_type']
        self._rows = {state: (row['greedy_action'], tuple(
            (row['actions'][action]['value'], row['actions'][action]['visits'])
            for action in (0, 1))) for state, row in rows.items()}

    def advise(self, observation):
        if (not isinstance(observation, (list, tuple)) or len(observation) != 3
                or type(observation[0]) is not int or not 4 <= observation[0] <= 21
                or type(observation[1]) is not int or not 1 <= observation[1] <= 10
                or type(observation[2]) is not bool):
            raise ValueError('Expected a nonterminal Foundations observation.')
        row = self._rows.get(tuple(observation))
        actions = row[1] if row else ((None, 0), (None, 0))
        supported = all(count > 0 for value, count in actions)
        return {'algorithm': self.algorithm, 'observation': list(observation),
                'action': row[0] if supported else None,
                'status': 'estimated' if supported else 'insufficient_evidence',
                'actions': [{'action': action, 'value': value, 'visits': count}
                            for action, (value, count) in enumerate(actions)],
                'note': 'Frozen estimates, not win probabilities or optimality guarantees. Advice is withheld if either action is unvisited.'}


def load_policy(path):
    return FrozenPolicy(json.loads(Path(path).read_text(encoding='utf-8')))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--total', type=int, required=True)
    parser.add_argument('--dealer', type=int, required=True)
    parser.add_argument('--soft', action='store_true')
    args = parser.parse_args()
    try:
        advice = load_policy(args.input).advise((args.total, args.dealer, args.soft))
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    print(json.dumps(advice, indent=2))


if __name__ == '__main__':
    main()
