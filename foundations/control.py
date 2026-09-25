"""Learn hit/stand decisions with first-visit, epsilon-greedy Monte Carlo control."""

import argparse
import json
import math
from pathlib import Path
import random

from foundations.blackjack import Blackjack, HIT, STAND
from foundations.monte_carlo import EpisodeStep, returns_from_episode, source_metadata

ACTIONS = (STAND, HIT)


def greedy_action(state, q):
    """Frozen evaluation: prefer stand on ties, including entirely unseen states."""
    return HIT if q.get((state, HIT), 0.0) > q.get((state, STAND), 0.0) else STAND


def epsilon_greedy(state, q, rng, epsilon):
    if rng.random() < epsilon:
        return rng.choice(ACTIONS)
    best = max(q.get((state, action), 0.0) for action in ACTIONS)
    # Randomize training ties so zero initialization does not always favor stand.
    return rng.choice([action for action in ACTIONS if q.get((state, action), 0.0) == best])


def update_action_values(episode, q, counts):
    """Each (state, action) receives its first-visit return once per episode."""
    seen = set()
    for step, sample_return in zip(episode, returns_from_episode(episode)):
        key = (step.observation, step.action)
        if key in seen:
            continue
        seen.add(key)
        counts[key] = counts.get(key, 0) + 1
        old = q.get(key, 0.0)
        q[key] = old + (sample_return - old) / counts[key]


def train(episodes, seed, epsilon):
    if episodes < 1:
        raise ValueError("Training episodes must be positive.")
    if not math.isfinite(epsilon) or not 0 <= epsilon <= 1:
        raise ValueError("Epsilon must be between 0 and 1.")
    env, rng = Blackjack(seed), random.Random(seed + 1)
    q, counts = {}, {}
    outcomes = {-1.0: 0, 0.0: 0, 1.0: 0}
    for _ in range(episodes):
        state, done, episode = env.reset(), False, []
        while not done:
            action = epsilon_greedy(state, q, rng, epsilon)
            next_state, reward, done = env.step(action)
            episode.append(EpisodeStep(state, action, reward))
            state = next_state
        # Keep Q fixed throughout this hand, then improve the next hand's policy.
        update_action_values(episode, q, counts)
        outcomes[sum(step.reward for step in episode)] += 1
    return q, counts, {"wins": outcomes[1.0], "losses": outcomes[-1.0],
                       "pushes": outcomes[0.0], "mean_return": (outcomes[1.0] - outcomes[-1.0]) / episodes}


def evaluate(q, episodes, seed, policy="greedy"):
    """Use fresh games and never update Q. The interval measures game sampling only."""
    if episodes < 2:
        raise ValueError("Evaluation needs at least two episodes.")
    if policy not in ("greedy", "threshold", "random"):
        raise ValueError("Unknown evaluation policy.")
    env, rng = Blackjack(seed), random.Random(seed + 1)
    outcomes = {-1.0: 0, 0.0: 0, 1.0: 0}
    unvisited = decisions = 0
    for _ in range(episodes):
        state, done, total = env.reset(), False, 0.0
        while not done:
            decisions += 1
            if policy == "greedy":
                action = greedy_action(state, q)
                unvisited += (state, action) not in q
            elif policy == "threshold":
                action = HIT if state[0] < 17 else STAND
            else:
                action = rng.choice(ACTIONS)
            state, reward, done = env.step(action)
            total += reward
        outcomes[total] += 1
    mean = (outcomes[1.0] - outcomes[-1.0]) / episodes
    variance = max(0.0, (outcomes[1.0] + outcomes[-1.0] - episodes * mean * mean) / (episodes - 1))
    se = math.sqrt(variance / episodes)
    return {"policy": policy, "seed": seed, "episodes": episodes,
            "wins": outcomes[1.0], "losses": outcomes[-1.0], "pushes": outcomes[0.0],
            "mean_return": mean, "standard_error": se,
            "approx_95pct_interval": [mean - 1.96 * se, mean + 1.96 * se],
            "decisions": decisions, "unvisited_selected_actions": unvisited if policy == "greedy" else None}


def experiment(episodes, eval_episodes, seed, eval_seed, epsilon):
    if seed == eval_seed:
        raise ValueError("Use different training and evaluation seeds.")
    q, counts, training = train(episodes, seed, epsilon)
    evaluations = [evaluate(q, eval_episodes, eval_seed, policy) for policy in ("greedy", "threshold", "random")]
    states = sorted({state for state, action in q})
    return {"schema_version": 1, "artifact_type": "monte_carlo_control",
            "rules": "foundations-v1: replacement draws, S17, no natural bonus, hit/stand",
            "algorithm": "first-visit on-policy epsilon-greedy Monte Carlo control", "gamma": 1.0,
            "training": {"episodes": episodes, "environment_seed": seed, "agent_seed": seed + 1,
                         "epsilon": epsilon, "outcomes": training},
            "evaluation": evaluations,
            "evaluation_note": "Frozen greedy policy; stand on ties; unseen action estimates initialize at zero. Intervals cover game sampling, not training-seed uncertainty. Equal evaluation seeds do not imply paired hands across policies.",
            "states": [{"observation": list(state), "greedy_action": greedy_action(state, q),
                        "actions": [{"action": action, "value": q.get((state, action)),
                                     "visits": counts.get((state, action), 0)} for action in ACTIONS]} for state in states]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=50000)
    parser.add_argument("--eval-episodes", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--eval-seed", type=int, default=1000007)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.eval_episodes < 2:
        parser.error("--eval-episodes must be at least 2")
    try:
        report = experiment(args.episodes, args.eval_episodes, args.seed, args.eval_seed, args.epsilon)
    except ValueError as error:
        parser.error(str(error))
    report["source"] = source_metadata()
    print(f"Training: {args.episodes} hands, seed={args.seed}, epsilon={args.epsilon}")
    print("Evaluation: frozen policies, fresh environment seed=" + str(args.eval_seed))
    for row in report["evaluation"]:
        low, high = row["approx_95pct_interval"]
        print(f"{row['policy']:9}: mean={row['mean_return']:+.4f}, approximate 95% interval [{low:+.4f}, {high:+.4f}]")
    print("Selected learned decisions (0=stand, 1=hit):")
    for row in report["states"]:
        if row["observation"] in ([12, 6, False], [16, 10, False], [20, 10, False]):
            print(f"  {tuple(row['observation'])}: action={row['greedy_action']}, estimates={row['actions']}")
    print("Intervals reflect evaluation sampling only; repeat training seeds before generalizing.")
    print("Q estimates describe training experience; they are not win probabilities or proof of optimal play.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
        print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
