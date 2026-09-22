"""Optional rule checks against Gymnasium; no changes to the learning policies.

Install requirements-reference.txt first, then:
python3 -m foundations.check_reference --episodes 20000 --output /tmp/reference.json
"""

import argparse
from collections import Counter
from itertools import combinations_with_replacement
import json
import math
from pathlib import Path
import random
from unittest.mock import patch

from foundations.blackjack import Blackjack, HIT, STAND, RANK_VALUES, score_hand
from foundations.monte_carlo import source_metadata


def reference_module():
    try:
        from gymnasium.envs.toy_text import blackjack
    except ImportError as error:
        raise RuntimeError("Install optional checks: python3 -m pip install -r requirements-reference.txt") from error
    return blackjack


def check_hand_scores():
    reference = reference_module()
    assert Counter(RANK_VALUES) == Counter(reference.deck), "Rank probabilities differ"
    checked = 0
    for length in range(1, 7):
        for cards in combinations_with_replacement(range(1, 11), length):
            assert score_hand(cards) == (reference.sum_hand(cards), reference.usable_ace(cards)), cards
            checked += 1
    return checked


def check_scripted_transitions():
    reference = reference_module()
    # player hand, dealer hand, upcoming draws, actions. Inject identical cards
    # to compare rules independently of the libraries' different RNGs/reset order.
    cases = [
        ([10, 8], [1, 6], [], [STAND]),
        ([10, 8], [5, 6], [10], [HIT]),
        ([5, 6], [10, 6], [8, 10], [HIT, STAND]),
        ([1, 10], [5, 6], [10], [STAND]),
        ([1, 10], [10, 8], [], [STAND]),
        ([10, 7], [10, 8], [], [STAND]),
        ([1, 1], [10, 7], [9], [HIT, STAND]),
        ([1, 6], [10, 7], [10], [HIT, STAND]),
        ([10, 8], [10, 8], [], [STAND]),
        ([1, 10], [1, 10], [], [STAND]),
    ]
    transitions = 0
    for index, (player, dealer, draws, actions) in enumerate(cases):
        ours = Blackjack()
        ours.reset()
        ours._player, ours._dealer = list(player), list(dealer)
        other = reference.BlackjackEnv(natural=False, sab=False)
        other.reset(seed=0)
        other.player, other.dealer = list(player), list(dealer)
        with patch.object(ours, "_draw", side_effect=list(draws)) as local_draw:
            with patch.object(reference, "draw_card", side_effect=list(draws)) as ref_draw:
                assert ours._observation() == other._get_obs(), index
                for action in actions:
                    observation, reward, done = ours.step(action)
                    ref_observation, ref_reward, terminated, truncated, _ = other.step(action)
                    assert (observation, reward, done) == (ref_observation, ref_reward, terminated), index
                    assert not truncated, index
                    transitions += 1
                assert local_draw.call_count == ref_draw.call_count, index
                assert ours._player == other.player and ours._dealer == other.dealer, index
        other.close()
    return {"cases": len(cases), "transitions": transitions}


def sample_outcomes(implementation, policy, episodes, seed):
    reference = reference_module()
    env = Blackjack(seed) if implementation == "foundations" else reference.BlackjackEnv(natural=False, sab=False)
    agent_rng = random.Random(seed + 2000000)
    counts = {-1.0: 0, 0.0: 0, 1.0: 0}
    for index in range(episodes):
        if implementation == "foundations":
            observation = env.reset()
        else:
            observation, _ = env.reset(seed=seed if index == 0 else None)
        done = False
        total_return = 0.0
        while not done:
            action = agent_rng.choice((STAND, HIT)) if policy == "random" else (HIT if observation[0] < 17 else STAND)
            if implementation == "foundations":
                observation, reward, done = env.step(action)
            else:
                observation, reward, done, truncated, _ = env.step(action)
                assert not truncated
            total_return += reward
        counts[total_return] += 1
    if implementation != "foundations":
        env.close()
    mean = (counts[1.0] - counts[-1.0]) / episodes
    sum_squares = counts[1.0] + counts[-1.0]
    variance = max(0.0, (sum_squares - episodes * mean * mean) / (episodes - 1))
    return {"seed": seed, "episodes": episodes, "wins": counts[1.0],
            "losses": counts[-1.0], "pushes": counts[0.0], "mean_return": mean,
            "standard_error": math.sqrt(variance / episodes)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episodes", type=int, default=20000, help="Hands per policy, seed, and implementation")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.episodes < 2:
        parser.error("--episodes must be at least 2")
    try:
        reference_module()
    except RuntimeError as error:
        parser.error(str(error))
    import gymnasium
    import numpy
    report = {"source": source_metadata(), "gymnasium": gymnasium.__version__, "numpy": numpy.__version__,
              "rules": {"natural": False, "sab": False, "draws": "with replacement", "dealer": "stand on soft 17"},
              "hand_scores_checked": check_hand_scores(), "scripted": check_scripted_transitions(),
              "note": "Statistical differences are descriptive diagnostics, not an equivalence proof. Seeds differ across implementations; reference seed = foundations seed + 1000000.",
              "comparisons": []}
    print(f"Hand-score checks: {report['hand_scores_checked']}; scripted checks: {report['scripted']}")
    for policy in ("random", "threshold"):
        for seed in (7, 19, 42, 101, 2026):
            ours = sample_outcomes("foundations", policy, args.episodes, seed)
            reference = sample_outcomes("gymnasium", policy, args.episodes, seed + 1000000)
            difference = ours["mean_return"] - reference["mean_return"]
            difference_se = math.hypot(ours["standard_error"], reference["standard_error"])
            report["comparisons"].append({"policy": policy, "foundations": ours, "gymnasium": reference,
                                          "mean_difference": difference, "difference_standard_error": difference_se})
            print(f"{policy:9} seed={seed:4}: ours={ours['mean_return']:+.4f}, "
                  f"reference={reference['mean_return']:+.4f}, difference={difference:+.4f}, SE={difference_se:.4f}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n")
        print(f"Saved {args.output}")


if __name__ == "__main__":
    main()
