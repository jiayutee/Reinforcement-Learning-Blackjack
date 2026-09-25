# Lesson 3: learn which action to take

Goal: move from predicting outcomes to changing decisions. This is **Monte Carlo control**, not Q-learning: the letter Q names an action-value function, and several algorithms can learn it.

Prerequisites: [Lesson 1](01-agent-environment.md) for observations/actions/rewards and [Lesson 2](02-monte-carlo-prediction.md) for completed-hand returns and incremental means. No extra dependencies are needed. Allow about 30 minutes.

## 1. Run the learning player

From the project folder:

```sh
python3 -m foundations.control --episodes 50000 --eval-episodes 20000 --seed 7 --eval-seed 1000007 --epsilon 0.1
```

The program trains for 50,000 hands, then stops updating its estimates and evaluates three policies on fresh games. The learned **greedy** policy chooses its highest estimated action value. The threshold baseline still hits below 17. The random baseline still chooses 50/50.

This uses the same simplified rules as earlier lessons: replacement draws, hit/stand only, dealer stands on soft 17, no natural bonus. The real six-deck web game is not implemented by this command.

## 2. Why V is not enough

Previously, `V(s)` estimated the expected return of following one fixed policy from position `s`. It gave us one number per position.

To choose between hit and stand, learn two numbers:

```text
Q(s, hit)   = expected return after hitting, then following the policy
Q(s, stand) = expected return after standing
```

The remaining policy matters: Q is not an intrinsic property of the cards. In control, the behavior policy changes as estimates improve, so the running means contain experience collected under earlier policies too. We do not claim every finite-sample Q entry is the exact value of the final greedy policy.

Suppose the estimates are:

```text
Q(s, hit)   = -0.40
Q(s, stand) = -0.60
```

Choose hit when exploiting: -0.40 is larger. Both choices can have negative expected return. Learning seeks the better action, not a guarantee of winning or positive profit.

## 3. Exploration versus exploitation

If we always choose the action that currently looks best, an unlucky early sample can make us abandon a useful alternative. **Exploration** deliberately samples actions. **Exploitation** uses current estimates.

Our epsilon-greedy rule uses `epsilon = 0.1`:

- With probability 0.1, choose uniformly between hit and stand.
- Otherwise, choose an action with the largest estimated Q.

If there is one best action, its total probability is `0.9 + 0.1/2 = 0.95`; the other action gets `0.1/2 = 0.05`. Exploration can choose the best action too! If estimates tie, training chooses uniformly among the tied actions, yielding 50/50 for two actions.

Epsilon stays constant in this introductory implementation. It preserves exploration but does not establish convergence to an optimal deterministic policy. We will study schedules and broader comparisons later rather than silently tuning parameters until one run looks good.

## 4. Update a state-action pair

Wait until the hand ends. For each distinct `(state, action)` first encountered in that hand, calculate its remaining return G and update:

```text
N(s,a) <- N(s,a) + 1
Q(s,a) <- Q(s,a) + [G - Q(s,a)] / N(s,a)
```

This is the same incremental mean as Lesson 2, but the dictionary key now includes the action. Hitting at 16 and standing at 16 have separate counts and estimates.

Example: hit has two previous samples, +1 and -1, so its count is 2 and its mean is 0. Another hit sample returns -1:

```text
N(hit) = 3
Q(hit) = 0 + (-1 - 0)/3 = -1/3
```

The stand estimate is untouched. A zero-return push still counts as a sample.

First-visit means once per **state-action pair** per episode, not just once per state. The implementation computes returns backward and selects first visits forward. Q stays fixed during a hand and is updated after completion; the next hand uses the improved estimates.

## 5. Read the code in order

Open [foundations/control.py](../../foundations/control.py):

1. `greedy_action`: compare the two action estimates.
2. `epsilon_greedy`: add random exploration and random training tie-breaking.
3. `update_action_values`: update counts and means from a completed episode.
4. `train`: repeat those steps across hands.
5. `evaluate`: play new games without changing Q.

The core update uses a nested tuple as the dictionary key:

```python
key = (step.observation, step.action)
counts[key] = counts.get(key, 0) + 1
old = q.get(key, 0.0)
q[key] = old + (sample_return - old) / counts[key]
```

For example, `((16, 10, False), 1)` means hard 16 against dealer 10, choosing hit. Missing estimates initialize at zero for choosing actions; this is an initialization convention, not evidence that an untried action has zero value. The JSON export marks unvisited action values as `null` with count 0.

## 6. Training and evaluation answer different questions

Training includes deliberate exploratory actions and changes the policy. Its average return is not an estimate of the final frozen greedy player's performance.

Evaluation creates a fresh environment with a different seed, uses no exploration for the learned policy, and never updates Q. Evaluation ties prefer stand, including a completely unseen state. The report counts selected actions that had no training visits so this fallback is visible.

Each evaluation reports its mean return and an approximate 95% interval:

```text
standard error = sample standard deviation / sqrt(number of hands)
interval      = mean +/- 1.96 * standard error
```

These large-sample normal intervals describe game-outcome sampling for one frozen policy. They do not include variation from training different agents. The independent-hand assumption fits the replacement-draw environment; do not reuse it blindly for correlated hands in a persistent finite shoe.

All three policies use the same evaluation seed for reproducibility, but their actions consume different numbers of cards. These are not paired identical hands, and individual intervals are not an interval for the difference between policies.

The first seed-7 sample is recorded in [today's note](../daily/2026-09-25.md). Treat it as an initial demonstration; the next checkpoint will repeat training with several seeds before generalizing.

## 7. Inspect or export the result

The CLI prints selected learned decisions and their per-action visit counts. Do not mistake them for a certified blackjack strategy. Rare actions and nearly tied estimates can produce unstable choices.

```sh
python3 -m foundations.control --episodes 50000 --eval-episodes 20000 --seed 7 --eval-seed 1000007 --epsilon 0.1 --output /tmp/blackjack-control.json
```

The export records action values, visits, decisions, rules, training/evaluation settings, and source provenance. This is a distinct artifact from Lesson 2's state-value export. The old value-map renderer deliberately does not accept it; an action-policy view will be a separate small integration.

## 8. Exercises

1. With a unique best action and epsilon 0.2, what probability does each action get?
2. An action has Q=0.25 after four samples. Its next sample is -1. Calculate the new mean.
3. If Q(hit)=-0.3 and Q(stand)=-0.5, which is greedy? Does that imply a profitable position?
4. Why must the evaluation loop avoid calling `update_action_values`?
5. Find `greedy_action` and explain what happens when neither action has ever been visited.

Try before reading [the separate answers](solutions/03-monte-carlo-control.md). Keep the experiment defaults unchanged for now so we can compare independent runs without selecting only favorable results.
