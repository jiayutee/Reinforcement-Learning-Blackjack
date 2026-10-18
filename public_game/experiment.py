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


def run_prediction(episodes=1000, seed=7, top=12):
    """Estimate V(s) for the threshold policy from complete sampled rounds."""
    if type(episodes) is not int or episodes <= 0:
        raise ValueError('episodes must be a positive integer')
    if type(top) is not int or top < 0:
        raise ValueError('top must be a nonnegative integer')
    from public_game.monte_carlo import FirstVisitMonteCarlo
    session = PublicSession(balance=episodes * 40 + 200, seed=seed)
    learner = FirstVisitMonteCarlo(gamma=1.0)
    for _ in range(episodes):
        learner.update(collect_round(session, threshold_policy, stake=20))
    estimates = sorted(learner.estimates.items(),
                       key=lambda item: (-item[1].count, repr(item[0])))
    shown = estimates[:top] if top else estimates
    return {
        'episodes': learner.episodes,
        'decision_episodes': learner.decision_episodes,
        'opening_naturals': learner.opening_terminals,
        'seed': seed,
        'policy': 'hit below17 else stand; ignores soft/pair context',
        'gamma': learner.gamma,
        'estimated_states': len(estimates),
        'reported_states': len(shown),
        'estimates': [
            {'state': list(key), 'count': estimate.count, 'value': estimate.value}
            for key, estimate in shown
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episodes', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--top', type=int, default=12,
                        help='show the most visited states (0 shows all)')
    parser.add_argument('--predict', action='store_true',
                        help='estimate state values by first-visit Monte Carlo')
    args = parser.parse_args()
    try:
        runner = run_prediction if args.predict else run_experiment
        if args.predict:
            result = runner(args.episodes, args.seed, args.top)
        else:
            result = runner(args.episodes, args.seed)
        print(json.dumps(result, indent=2, sort_keys=True))
    except ValueError as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
