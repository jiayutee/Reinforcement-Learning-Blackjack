# First-visit Monte Carlo exercise answers

1. In the first round, rewards are `[0, +1]`. With `gamma=1`, the second decision's return is `G_1=+1`; stepping backward gives the first decision `G_0=0+1=+1`. So both states receive a `+1` sample.
2. In the second round, `[0, -1]` gives return `-1` to both states. Each state has now supplied two samples: `(+1 + -1)/2 = 0` initial wagers. Both estimates are zero.
3. First-visit MC defines one sample per state per episode: the completed episode has one shared terminal outcome, and repeated visits are not independent outcomes. Updating only the first occurrence avoids counting the same round result multiple times for a state and biasing its estimate toward episodes where the policy loops through that state.

The tests use this exact two-round example and a duplicate-state episode to demonstrate both rules.
