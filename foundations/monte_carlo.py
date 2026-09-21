"""First-visit Monte Carlo prediction for a fixed blackjack policy.

Run: python3 -m foundations.monte_carlo --episodes 10000 --seed 7 --trace
Only the value estimates learn; the player's threshold policy stays fixed.
"""

import argparse
import json
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, NamedTuple

from foundations.blackjack import Blackjack, HIT, STAND, Observation


class EpisodeStep(NamedTuple):
    observation: Observation
    action: int
    reward: float


def record_episode(env: Blackjack, threshold: int) -> List[EpisodeStep]:
    """Keep observations before actions; terminal observations aren't decisions."""
    episode = []
    observation = env.reset()
    done = False
    while not done:
        action = HIT if observation[0] < threshold else STAND
        next_observation, reward, done = env.step(action)
        episode.append(EpisodeStep(observation, action, reward))
        observation = next_observation
    return episode


def returns_from_episode(episode: List[EpisodeStep]) -> List[float]:
    """G_t is the sum of rewards from this decision onward; gamma is 1."""
    returns = [0.0] * len(episode)
    total = 0.0
    for index in range(len(episode) - 1, -1, -1):
        total += episode[index].reward
        returns[index] = total
    return returns


def update_first_visit(
    episode: List[EpisodeStep],
    values: Dict[Observation, float],
    counts: Dict[Observation, int],
) -> None:
    """Update each state's mean once per hand, from its earliest occurrence."""
    returns = returns_from_episode(episode)
    seen = set()
    for step, sample_return in zip(episode, returns):
        state = step.observation
        if state in seen:
            continue
        seen.add(state)
        counts[state] = counts.get(state, 0) + 1
        previous = values.get(state, 0.0)
        values[state] = previous + (sample_return - previous) / counts[state]


def estimate_values(episodes: int, seed: int, threshold: int) -> dict:
    if episodes < 1:
        raise ValueError("episodes must be positive")
    if not 4 <= threshold <= 21:
        raise ValueError("threshold must be between 4 and 21")
    env = Blackjack(seed=seed)
    values = {}
    counts = {}
    outcomes = {-1.0: 0, 0.0: 0, 1.0: 0}
    first_episode = []
    for index in range(episodes):
        episode = record_episode(env, threshold)
        if index == 0:
            first_episode = episode
        update_first_visit(episode, values, counts)
        outcomes[sum(step.reward for step in episode)] += 1

    return {
        "schema_version": 1,
        "rules": "foundations-v1: replacement draws, S17, no natural bonus, hit/stand",
        "observation_fields": ["player_total", "dealer_upcard", "usable_ace"],
        "estimator": "first-visit Monte Carlo state-value prediction",
        "gamma": 1.0,
        "policy": {"name": "threshold", "hit_below": threshold, "learned": False},
        "seed": seed,
        "episodes": episodes,
        "wins": outcomes[1.0],
        "losses": outcomes[-1.0],
        "pushes": outcomes[0.0],
        "mean_return": (outcomes[1.0] - outcomes[-1.0]) / episodes,
        "first_episode": [
            {"observation": list(step.observation), "action": step.action,
             "reward": step.reward, "return": sample_return}
            for step, sample_return in zip(first_episode, returns_from_episode(first_episode))
        ],
        "states": [
            {"observation": list(state), "visits": counts[state], "value": values[state]}
            for state in sorted(values)
        ],
    }


def source_metadata() -> dict:
    """Report source provenance; missing git is explicit, not a fake revision."""
    root = Path(__file__).resolve().parents[1]
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, stderr=subprocess.DEVNULL
        ).strip()
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain", "--", "foundations"],
            cwd=root, text=True, stderr=subprocess.DEVNULL,
        ).strip())
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = None, None
    return {"python": platform.python_version(), "git_commit": revision,
            "foundations_source_dirty": dirty}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--threshold", type=int, default=17)
    parser.add_argument("--trace", action="store_true", help="Explain the first hand's updates")
    parser.add_argument("--output", type=Path, help="Save the full estimates and metadata as JSON")
    args = parser.parse_args()
    if args.episodes < 1:
        parser.error("--episodes must be positive")
    if not 4 <= args.threshold <= 21:
        parser.error("--threshold must be between 4 and 21")
    report = estimate_values(args.episodes, args.seed, args.threshold)
    report["source"] = source_metadata()

    print(f"Fixed policy: hit below {args.threshold}, otherwise stand")
    print(f"First-visit Monte Carlo; seed={args.seed}, episodes={args.episodes}, gamma=1")
    if args.trace:
        print("\nFirst completed hand (updates start only after it ends):")
        for step in report["first_episode"]:
            name = "hit" if step["action"] == HIT else "stand"
            print(f"  {tuple(step['observation'])}: {name}, reward={step['reward']:+.0f}, "
                  f"return={step['return']:+.0f}")
        print("  Each first-visited state starts at N=0, V=0; its first update sets V=return.")

    print(f"\nWins={report['wins']}, losses={report['losses']}, pushes={report['pushes']}")
    print(f"Mean return={report['mean_return']:+.4f} units/hand (descriptive sample only)")
    print(f"Observed decision states: {len(report['states'])}")
    print("\nSelected estimates: state -> value, first-visit count")
    states = {tuple(row["observation"]): row for row in report["states"]}
    for state in [(16, 10, False), (20, 10, False), (13, 2, True)]:
        row = states.get(state)
        if row is None:
            print(f"  {state} -> unknown (0 visits)")
        else:
            print(f"  {state} -> {row['value']:+.4f}, N={row['visits']}")
    print("Values describe the fixed policy, not win probabilities or best-action advice.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Saved estimates to {args.output}")


if __name__ == "__main__":
    main()
