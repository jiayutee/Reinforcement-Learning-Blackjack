"""Off-policy, one-step Q-learning for the Foundations blackjack rules."""
import argparse
import json
import math
import random
from pathlib import Path

from foundations.blackjack import Blackjack
from foundations.control import ACTIONS, epsilon_greedy, evaluate, greedy_action
from foundations.monte_carlo import source_metadata


def update(q, state, action, reward, next_state, done, alpha):
    """Use the largest next action estimate. Gamma is one."""
    key = (state, action)
    old = q.get(key, 0.0)
    bootstrap = 0.0 if done else max(q.get((next_state, a), 0.0) for a in ACTIONS)
    target = reward + bootstrap
    q[key] = old + alpha * (target - old)
    return {"old_value": old, "bootstrap": bootstrap, "target": target,
            "td_error": target - old, "new_value": q[key]}


def train(episodes, seed, epsilon=0.1, alpha=0.1):
    if episodes < 1:
        raise ValueError("episodes must be positive")
    if not math.isfinite(epsilon) or not 0 <= epsilon <= 1:
        raise ValueError("epsilon must be in [0, 1]")
    if not math.isfinite(alpha) or not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    env, rng = Blackjack(seed), random.Random(seed + 1)
    q, counts, trace = {}, {}, []
    outcomes = {-1.0: 0, 0.0: 0, 1.0: 0}
    for episode in range(episodes):
        state = env.reset()
        total = 0.0
        while True:
            action = epsilon_greedy(state, q, rng, epsilon)
            next_state, reward, done = env.step(action)
            numbers = update(q, state, action, reward, next_state, done, alpha)
            counts[(state, action)] = counts.get((state, action), 0) + 1
            if episode == 0:
                trace.append({"state": list(state), "action": action, "reward": reward,
                              "next_state": list(next_state),
                              "done": done, **numbers})
            total += reward
            if done:
                break
            state = next_state
        outcomes[total] += 1
    return q, counts, {"wins": outcomes[1.0], "losses": outcomes[-1.0],
                       "pushes": outcomes[0.0], "mean_return": (outcomes[1.0]-outcomes[-1.0])/episodes}, trace


def experiment(episodes, eval_episodes, seed, eval_seed, epsilon, alpha):
    if seed == eval_seed:
        raise ValueError("Use different training and evaluation seeds")
    if eval_episodes < 2:
        raise ValueError("Evaluation needs at least two episodes")
    q, counts, outcomes, trace = train(episodes, seed, epsilon, alpha)
    return {"schema_version": 1, "artifact_type": "q_learning_control",
            "rules": "foundations-v1: replacement draws, S17, no natural bonus, hit/stand",
            "algorithm": "one-step off-policy Q-learning", "gamma": 1.0,
            "training": {"episodes": episodes, "environment_seed": seed, "agent_seed": seed+1,
                         "alpha": alpha, "epsilon": epsilon, "outcomes": outcomes},
            "first_episode": trace,
            "evaluation": [evaluate(q, eval_episodes, eval_seed, policy)
                           for policy in ("greedy", "threshold", "random")],
            "evaluation_note": "Frozen greedy policy differs from exploratory training behavior. Stand on ties; unseen Q initializes at zero. Intervals cover game sampling only. Equal evaluation seeds do not imply paired hands across policies.",
            "states": [{"observation": list(s), "greedy_action": greedy_action(s, q),
                        "actions": [{"action": a, "visits": counts.get((s, a), 0),
                                     "value": q.get((s, a))} for a in ACTIONS]}
                       for s in sorted({s for s, a in q})]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=50000)
    parser.add_argument("--eval-episodes", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--eval-seed", type=int, default=1000007)
    parser.add_argument("--epsilon", type=float, default=0.1)
    parser.add_argument("--alpha", type=float, default=0.1)
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        report = experiment(args.episodes, args.eval_episodes, args.seed,
                            args.eval_seed, args.epsilon, args.alpha)
    except ValueError as error:
        parser.error(str(error))
    report["source"] = source_metadata()
    print(f"Q-learning: {args.episodes} training hands, epsilon={args.epsilon}, alpha={args.alpha}")
    if args.trace:
        for step in report["first_episode"]:
            print(json.dumps(step))
    for row in report["evaluation"]:
        print(f"{row['policy']}: mean={row['mean_return']:+.5f}, approximate 95% interval={row['approx_95pct_interval']}")
    print("Single-seed evaluation is preliminary; constant alpha/epsilon do not establish optimality.")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
