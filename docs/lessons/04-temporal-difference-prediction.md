# Lesson 4: learn before the hand ends with TD(0)

## Before you start

You need Python 3.9+, dictionaries, a loop, and basic arithmetic. No packages are required. Review [agent/environment](01-agent-environment.md) and [Monte Carlo prediction](02-monte-carlo-prediction.md) if these terms are unfamiliar:

- **State**: our observation `(player total, dealer upcard, usable ace)`. A usable ace currently counts as 11 without busting.
- **Policy**: a rule choosing actions. Here: hit below 17, otherwise stand. This rule stays fixed.
- **Reward**: +1 for a win, -1 for a loss, 0 for a push or an unfinished hit.
- **Return**: all rewards remaining in a hand. Here only the ending reward is nonzero.
- **Value V(s)**: expected return starting in state s while following that policy. It is not a win probability.

The environment samples ranks with replacement, dealer stands on soft 17, and there are no splits, doubles, or natural bonuses. This lesson predicts values; it does not improve playing decisions. [Lesson 3](03-monte-carlo-control.md) learned decisions using Monte Carlo. We temporarily return to prediction to isolate one new idea before SARSA and Q-learning.

## Intuition: learn from your current prediction

Monte Carlo waits for the final outcome and uses the actual return as its target. Temporal-difference learning can update after one action. After a nonterminal hit, use the immediate reward plus your current estimate of what comes next. Using an estimate inside another estimate is called **bootstrapping**.

An estimate may initially be wrong. Repeated experience helps correct it, but TD is not guaranteed to beat Monte Carlo in every experiment. TD(0) means one-step TD, with no eligibility trace carrying credit across earlier states.

## Equations, one step at a time

Let s be the state before an action, r the reward, and s' the next observation. Let alpha be the learning rate and gamma the discount factor. We use gamma = 1 because these are finite hands and we count the full outcome.

1. For an unfinished hand, target = r + gamma * V(s').
2. For a finished hand, target = r. There is no future reward after termination.
3. TD error delta = target - V(s).
4. Update V(s) = V(s) + alpha * delta.

Here alpha = 0.1 moves one tenth of the distance toward the target. Equivalently, new V = 0.9 * old V + 0.1 * target. This fixed learning rate is **not** the Monte Carlo sample-mean step size 1/N. Its estimates keep responding to recent targets; visits do not turn it into an arithmetic mean. Constant alpha generally leaves sampling fluctuations rather than guaranteeing exact convergence. Standard convergence results need additional conditions, including suitable decreasing step sizes and repeated state visits.

### Worked arithmetic

Suppose V(s) = 0.2 and a nonterminal hit reaches s' with V(s') = 0.6, reward 0:

- target = 0 + 1 * 0.6 = 0.6
- delta = 0.6 - 0.2 = 0.4
- new V(s) = 0.2 + 0.1 * 0.4 = **0.24**

If instead the hand ends in a loss, target = -1 and new V(s) = 0.2 + 0.1 * (-1 - 0.2) = **0.08**. Ignore any value stored under the returned observation. In this environment, standing can return the same player observation, but `done=True` means it must not bootstrap from itself. A terminal push similarly has target zero; an unfinished reward of zero can still bootstrap.

### Why the first hit may learn nothing

Start every value at zero. A hand goes A --hit, reward 0--> B --stand, reward +1--> terminal.

With alpha = 0.1, the A update uses the current V(B)=0, so V(A) stays 0. The later terminal update makes V(B)=0.1. We do not go back and redo A. On a later A-to-B transition, A can learn 0.01 from that estimate. Monte Carlo would wait for the win and update both first-visited states toward +1 in the first hand. This difference explains how information propagates across visits.

## Read the code in order

Open [foundations/td.py](../../foundations/td.py).

1. `update_value` reads `old` and `bootstrap` before changing the dictionary. `values.get(state, 0.0)` implements zero initialization.
2. `done` selects zero bootstrap for terminal transitions. Then `target`, `error`, and the assignment directly implement the equations.
3. `estimate_values` creates one seeded environment and empty value/count dictionaries.
4. Each loop chooses the fixed threshold action, calls `env.step`, and updates immediately. Only then does `state = next_state` advance the loop.
5. `counts` records updates, not confidence or independent samples. Unlike first-visit MC, this code updates every transition; no `seen` set is needed.
6. The first-hand trace saves the numbers at update time, so later learning cannot rewrite its history.

The JSON artifact is explicitly `td_prediction`. Existing Monte Carlo value-map and action-table renderers intentionally reject it; we must label different estimators accurately before adapting visual tools.

## Run and compare

From the project root:

```sh
python3 -m foundations.td --episodes 10000 --seed 7 --alpha 0.1 --trace --output /tmp/blackjack-td.json
python3 -m foundations.monte_carlo --episodes 10000 --seed 7 --threshold 17 --output /tmp/blackjack-mc.json
python3 -m unittest discover -s tests -v
```

Both algorithms follow exactly the same fixed policy and consume the same seeded environment draws here. Their game outcomes should match: 4,009 wins, 4,922 losses, 1,069 pushes, mean return -0.0913. Values differ because the updates differ. Changing alpha alone does not improve this player's decisions.

At seed 7, 10,000 hands, TD alpha 0.1 gives hard 16 vs 10 about -0.489325 (407 updates), hard 20 vs 10 +0.413449 (507), and soft 13 vs 2 -0.072062 (14). These are descriptive results, not known ground truth. A difference from MC does not establish which estimate is more accurate. Rare states and constant-alpha fluctuations matter.

Try alpha 0.05 with everything else unchanged. Predict what will stay identical before running it. Do not select a learning rate by whichever estimate looks more optimistic.

## Exercise and comprehension check

1. V(s)=-0.4, V(s')=0.2, r=0, alpha=0.25, gamma=1, unfinished hand. Compute target, error, and new value.
2. Repeat for a terminal push. Why must the result differ?
3. Starting at zero, apply A-to-B reward 0 then B-to-terminal reward -1 with alpha=0.5. What are A and B afterward? What happens on the next A-to-B transition?
4. Does a higher observed V automatically cause this agent to stand? Explain.
5. Why is 14 updates insufficient evidence that a soft-state estimate is accurate? Why is 507 updates still not a guarantee?

[Separate answers](solutions/04-temporal-difference-prediction.md). Next: compare the estimators carefully, then introduce action-value bootstrapping with SARSA. The browser game remains a separate unfinished milestone.
