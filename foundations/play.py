"""Run with: python3 -m foundations.play --seed 7 --episodes 3"""

import argparse
import random

from foundations.blackjack import Blackjack, HIT, STAND


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--episodes", type=int, default=3)
    parser.add_argument("--policy", choices=("random", "threshold"), default="random")
    parser.add_argument("--quiet", action="store_true", help="Print only the summary")
    args = parser.parse_args()
    if args.episodes < 1:
        parser.error("--episodes must be positive")

    env = Blackjack(seed=args.seed)
    # Agent randomness must not consume the environment's random stream.
    agent_rng = random.Random(args.seed + 1)
    results = {-1.0: 0, 0.0: 0, 1.0: 0}
    for episode in range(args.episodes):
        observation = env.reset()
        done = False
        episode_return = 0.0
        if not args.quiet:
            print(f"\nHand {episode + 1}: observation={observation}")
        while not done:
            if args.policy == "random":
                action = agent_rng.choice((STAND, HIT))
            else:
                action = HIT if observation[0] < 17 else STAND
            next_observation, reward, done = env.step(action)
            episode_return += reward
            if not args.quiet:
                name = "hit" if action == HIT else "stand"
                print(f"  {observation} -> {name} -> {next_observation}; "
                      f"reward={reward:+.0f}, done={done}")
            observation = next_observation
        results[episode_return] += 1

    mean_return = (results[1.0] - results[-1.0]) / args.episodes
    print(f"\nPolicy={args.policy}, seed={args.seed}, hands={args.episodes}")
    print(f"Wins={results[1.0]}, losses={results[-1.0]}, pushes={results[0.0]}")
    print(f"Mean return={mean_return:+.4f} units/hand (descriptive sample only)")


if __name__ == "__main__":
    main()
