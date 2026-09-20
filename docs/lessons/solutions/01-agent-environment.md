# Lesson 1 worked answers

1. The player cannot see it. Giving it to the agent would let the agent exploit information unavailable during legitimate play.
2. Reward is feedback for one transition; return adds rewards over time. Here we use an undiscounted sum over a hand.
3. No. It can mean an unfinished hand or a terminal push. Read `done`.
4. A seed reproduces a random stream given the same implementation/runtime and sequence of calls. It does not prove a policy is good or make different policies encounter identical hands.
5. The random player never updates its decisions from experience. Learning requires an update mechanism; we will add one next.

Threshold exercise: hitting on 17 can lead to a higher total or a bust. A measured difference from one seed is an observation, not a universal conclusion. The dealer upcard and usable ace can also matter, which a single threshold ignores.
