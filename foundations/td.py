"""TD(0) state-value prediction under the fixed hit-below-threshold policy."""
import argparse
import json
import math
from pathlib import Path

from foundations.blackjack import Blackjack, HIT, STAND
from foundations.monte_carlo import source_metadata


def update_value(values, state, reward, next_state, done, alpha):
    """One online update, gamma=1. A terminal observation never bootstraps."""
    old = values.get(state, 0.0)
    bootstrap = 0.0 if done else values.get(next_state, 0.0)
    target = reward + bootstrap
    error = target - old
    values[state] = old + alpha * error
    return {"old_value": old, "bootstrap": bootstrap, "target": target,
            "td_error": error, "new_value": values[state]}


def estimate_values(episodes, seed, threshold=17, alpha=0.1):
    if episodes < 1:
        raise ValueError("episodes must be positive")
    if not 4 <= threshold <= 21:
        raise ValueError("threshold must be between 4 and 21")
    if not math.isfinite(alpha) or not 0 < alpha <= 1:
        raise ValueError("alpha must be finite and in (0, 1]")
    env = Blackjack(seed)
    values, counts, first_episode = {}, {}, []
    outcomes = {-1.0: 0, 0.0: 0, 1.0: 0}
    for index in range(episodes):
        state, done, total = env.reset(), False, 0.0
        while not done:
            action = HIT if state[0] < threshold else STAND
            next_state, reward, done = env.step(action)
            update = update_value(values, state, reward, next_state, done, alpha)
            counts[state] = counts.get(state, 0) + 1
            if index == 0:
                first_episode.append({"observation": list(state), "action": action,
                    "reward": reward, "next_observation": list(next_state),
                    "done": done, **update})
            total += reward
            state = next_state
        outcomes[total] += 1
    return {"schema_version": 1, "artifact_type": "td_prediction",
        "rules": "foundations-v1: replacement draws, S17, no natural bonus, hit/stand",
        "estimator": "online TD(0) state-value prediction", "gamma": 1.0,
        "alpha": alpha, "initial_value": 0.0,
        "policy": {"name": "threshold", "hit_below": threshold, "learned": False},
        "episodes": episodes, "seed": seed,
        "wins": outcomes[1.0], "losses": outcomes[-1.0], "pushes": outcomes[0.0],
        "mean_return": (outcomes[1.0] - outcomes[-1.0]) / episodes,
        "first_episode": first_episode,
        "states": [{"observation": list(state), "visits": counts[state],
                    "value": values[state]} for state in sorted(values)]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--threshold", type=int, default=17)
    parser.add_argument("--alpha", type=float, default=0.1)
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = estimate_values(args.episodes, args.seed, args.threshold, args.alpha)
    except ValueError as error:
        parser.error(str(error))
    report["source"] = source_metadata()
    print(f"TD(0): fixed hit-below-{args.threshold}, alpha={args.alpha}, gamma=1")
    print(f"Hands={args.episodes}, seed={args.seed}, mean return={report['mean_return']:+.4f}")
    if args.trace:
        print("First hand: updates happen immediately after each action:")
        for row in report["first_episode"]:
            print(f"  {tuple(row['observation'])}, action={row['action']}, done={row['done']}: "
                  f"target=({row['reward']:+.2f}) + ({row['bootstrap']:+.2f}) = {row['target']:+.2f}; "
                  f"V {row['old_value']:+.2f} -> {row['new_value']:+.2f}")
    for row in report["states"]:
        if row["observation"] in ([16, 10, False], [20, 10, False], [13, 2, True]):
            print(f"  {tuple(row['observation'])}: V={row['value']:+.6f}, updates={row['visits']}")
    print("The policy does not learn. Constant-alpha values are not sample means or win probabilities.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
