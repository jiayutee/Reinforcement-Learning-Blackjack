# Lesson 2: learn a value by averaging experience

**Goal:** estimate how good a blackjack position is while following a fixed policy. You will learn from completed hands, inspect the arithmetic, and understand why learning a value is different from learning which action to take.

Allow about 20–30 minutes. Start with [Lesson 1](01-agent-environment.md) if observation, action, reward, or episode is unfamiliar. This lesson still uses only Python's standard library.

## 1. Run it first

Open a terminal in `Reinforcement_Learning_Blackjack`:

```sh
python3 -m foundations.monte_carlo --episodes 10000 --seed 7 --trace
```

The player always hits below 17 and stands otherwise. That policy does not change during this experiment. The program **learns value estimates** from the outcomes it observes.

The first traced hand is:

```text
(9, 7, False): hit, reward=+0, return=+1
(20, 7, True): stand, reward=+1, return=+1
```

The draw was an ace: the player's total becomes 20 with a usable ace. The dealer eventually loses. Both decision positions receive a sample return of +1, because both were followed by the same win. No estimate is updated until the hand is complete.

These are simplified replacement-draw rules, not a six-deck casino simulation. Nothing is removed from a shoe, suits are not represented, and all future draws retain the same rank probabilities. This keeps the first value-learning problem small. The realistic game is a later milestone.

## 2. What are we estimating?

Let `s = (16, 10, False)`: the player has hard 16 and the dealer shows a ten-valued card. Ask:

> If I find myself in this position and keep following our fixed policy, what return should I expect on average?

Call that quantity `v_pi(s)`. The Greek letter `pi` means the policy. A different policy can have a different value for the same position. The implementation stores its estimate in `values[s]`, written mathematically as `V(s)`.

The formal definition is:

```text
v_pi(s) = E_pi[G_t | S_t = s]
```

Read it as: the average remaining return `G_t`, conditional on being in position `s`, when decisions follow policy `pi`. `E` means expectation: the probability-weighted average over possible outcomes. We do not know it in advance, so we estimate it using samples.

Here, observations are the positions whose values we learn. Replacement draws and the absence of natural bonuses make these compact positions sufficient for predicting future returns under this policy, without revealing the dealer's hidden card. A finite shoe would need more care about missing information.

With rewards +1 for a win, -1 for a loss, and 0 for a push:

```text
value = P(win from s under pi) - P(loss from s under pi)
```

A value of +0.4 is **not** a 40% win probability. For example, 60% wins, 20% losses, and 20% pushes gives value +0.4. Values can be negative.

## 3. Reward is immediate; return looks forward

For a hand ending after decision `T - 1`, the general return is:

```text
G_t = R_(t+1) + gamma * R_(t+2) + ... + gamma^(T-t-1) * R_T
```

`R_(t+1)` is the reward received after decision `t`. `gamma` is a discount factor: it controls how much later rewards count. We set **gamma = 1** so every reward in this finite hand counts fully. Then the return is simply the sum of remaining rewards.

In our blackjack environment, only the last action can produce a nonzero reward. That makes the remaining return equal to the final result for every decision in that hand. The code still calculates the sum explicitly, so the connection to the general definition is visible.

A terminal observation is not another decision to learn from. We record the observation **before** each action, along with that action and its reward. If hitting from 16 causes a bust at 26, the sample updates the value of 16; we do not add a decision state for 26.

## 4. Monte Carlo means learning from completed samples

Monte Carlo prediction collects complete episodes and averages their returns. It needs observed experience rather than a table of transition probabilities. It waits for actual outcomes instead of using another value estimate as its target.

For **first-visit** Monte Carlo, count a position once per hand, using the return following its earliest occurrence. If it appears in a later hand, that is another sample. This prevents longer visits within one episode from being counted as several independent episode samples. Different states from the same hand are still correlated; the rule does not make them independent.

Repeated identical decision observations are not needed for these blackjack examples. We nevertheless implement and test first-visit semantics so the algorithm remains correctly defined when you study other environments.

## 5. Work out the update by hand

Suppose one position is encountered in three separate hands, with returns:

```text
+1, -1, +1
```

After each hand:

| Samples N | New return G | Estimated value V |
|---|---|---|
| 1 | +1 | 1 |
| 2 | -1 | 0 |
| 3 | +1 | 1/3 |

You could keep every return and calculate their mean. Instead, use an incremental average:

```text
N(s) <- N(s) + 1
V(s) <- V(s) + [G - V(s)] / N(s)
```

`G - V(s)` is the difference between the observed outcome and the old estimate. Multiplying it by `1/N(s)` moves the estimate toward the new sample. Early samples move the estimate more; later samples move it less.

For the third sample, the old value is zero and `N=3`:

```text
new V = 0 + (1 - 0)/3 = 1/3
```

This update is exactly the sample mean, apart from floating-point rounding. Starting at zero does not add an imaginary sample: the first update uses `N=1` and replaces the estimate with the first return.

## 6. Read and understand the Python

Open [foundations/monte_carlo.py](../../foundations/monte_carlo.py) and follow these four functions in order:

1. `record_episode`: play one complete hand and record its decisions.
2. `returns_from_episode`: walk backward, accumulating future rewards.
3. `update_first_visit`: walk forward, updating each state's first occurrence.
4. `estimate_values`: repeat for many hands while keeping the same policy.

The backward return calculation is:

```python
total = 0.0
for index in range(len(episode) - 1, -1, -1):
    total += episode[index].reward
    returns[index] = total
```

The three arguments to `range` mean start at the last index, stop before -1, and move backward by one. `total += reward` means `total = total + reward`.

The numerical update is:

```python
counts[state] = counts.get(state, 0) + 1
previous = values.get(state, 0.0)
values[state] = previous + (sample_return - previous) / counts[state]
```

A dictionary maps a key to a value. The tuple `state` is a key, so `(16, 10, False)` and `(16, 10, True)` get different entries. `.get(state, 0)` returns the old count or zero when the state is new. A `seen` set remembers which states have already been updated in this hand; we create a fresh set for each episode.

Notice the ordering: returns are calculated backward, but first visits are selected **forward**. Updating only the first state encountered during a reverse walk would actually select the last visit.

## 7. Interpret the experiment carefully

For 10,000 hands, seed 7, and threshold 17, the current implementation produces:

| Position | Estimated value | First-visit samples |
|---|---:|---:|
| Hard 16 against 10 | -0.6167 | 407 |
| Hard 20 against 10 | +0.4221 | 507 |
| Soft 13 against 2 | -0.4286 | 14 |

The run has 4,009 wins, 4,922 losses, and 1,069 pushes. Its mean return is -0.0913 units per hand, the same as the earlier threshold baseline. That equality is expected: estimating values has not changed how the player acts.

The soft-13 estimate has only 14 samples. Do not treat it as equally reliable as the estimate based on 507 samples. An unvisited state is shown as **unknown**, not as a proven value of zero. Sample counts help identify scarce evidence; they are not a substitute for uncertainty intervals.

These estimates are descriptive results for one policy and one sample. We have not shown an optimal policy, a profitable strategy, formal statistical significance, or validation against Gymnasium. The dedicated evaluation lesson will introduce uncertainty and held-out evaluation. We do not rank algorithms from this single run.

## 8. Experiment without editing the baseline

Try more samples, then another seed:

```sh
python3 -m foundations.monte_carlo --episodes 100000 --seed 7
python3 -m foundations.monte_carlo --episodes 10000 --seed 42
```

Predict which positions will remain relatively rare. Record how the estimates and counts change. More samples generally improve estimation, but an individual estimate need not move smoothly toward its true value.

To study a different fixed policy:

```sh
python3 -m foundations.monte_carlo --episodes 10000 --seed 7 --threshold 18
```

This starts a **new table**. It does not mix returns from policies 17 and 18. Values are policy-specific. The same seed does not ensure identical deals across policies, because their different decisions may draw different numbers of cards.

Optional: export all observed state estimates for inspection or a future learning-lab view:

```sh
python3 -m foundations.monte_carlo --episodes 10000 --seed 7 --output /tmp/blackjack-values.json
```

The JSON includes rules, policy, seed, episode count, state visits, estimates, Python version, source commit, and whether the Foundations source has uncommitted changes. Unknown states have no entry. The export is a value table, **not a policy model that chooses between hit and stand**.

## 9. Exercises and comprehension check

1. Starting from an empty table, manually update one state's value for returns `+1, -1, 0, +1`. Write the count and value after each sample.
2. If one state is absent from the JSON, what can you conclude about its value?
3. Why does this lesson learn something while leaving the player's decisions unchanged?
4. Why do we wait until the episode ends to apply Monte Carlo updates?
5. If a position appears twice in a hypothetical hand, which occurrence supplies its first-visit return?
6. Coding exercise: add `(18, 6, False)` to the CLI's selected-state display. Find its full entry in the exported JSON and check that the displayed rounded value and count agree.

Try these before opening [the separate answers](solutions/02-monte-carlo-prediction.md).

Next: distinguish state values `V(s)` from action values `Q(s,a)`, then introduce exploration so the agent can learn which action to choose. First we will strengthen the environment/reference checks and the presentation of this lesson's results.
