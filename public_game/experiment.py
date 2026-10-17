"""Small reproducible fixed-policy experiment; this policy does not learn."""
import argparse
import json
from statistics import mean, pstdev

from public_game.episodes import collect_round
from public_game.session import PublicSession


def threshold_policy(observation):
    """Simple baseline: hit below17, otherwise stand. Ignores soft/pair context."""
    hand = observation['hands'][observation['active_hand']]
    return 'hit' if hand['total'] < 17 else 'stand'


def run_experiment(episodes=1000, seed=7):
    if type(episodes) is not int or episodes <= 0:
        raise ValueError('episodes must be a positive integer')
    session = PublicSession(balance=episodes * 40 + 200, seed=seed)
    outcomes, steps, naturals = [], 0, 0
    for _ in range(episodes):
        episode = collect_round(session, threshold_policy, stake=20)
        outcomes.append(episode.normalized_profit)
        steps += len(episode.transitions)
        naturals += episode.opening_terminal
    return {
        'episodes': episodes,
        'seed': seed,
        'policy': 'hit below17 else stand; ignores soft/pair context',
        'mean_normalized_profit': mean(outcomes),
        'population_sd': pstdev(outcomes),
        'wins': sum(x > 0 for x in outcomes),
        'losses': sum(x < 0 for x in outcomes),
        'pushes': sum(x == 0 for x in outcomes),
        'opening_naturals': naturals,
        'decision_transitions': steps,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episodes', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=7)
    args = parser.parse_args()
    try:
        print(json.dumps(run_experiment(args.episodes, args.seed), indent=2, sort_keys=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
