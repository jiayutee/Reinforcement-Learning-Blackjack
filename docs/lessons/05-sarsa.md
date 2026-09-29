# Lesson 5: SARSA learns from the next action it chooses

## Prerequisites and recap

Use Python 3.9+; no extra packages are required. You need loops, functions, dictionary keys, and arithmetic. Read [Lesson 3](03-monte-carlo-control.md) for action values and [Lesson 4](04-temporal-difference-prediction.md) for bootstrapping if these ideas are new.

A state is `(player total, dealer upcard, usable ace)`. An action is stand (0) or hit (1). Reward is +1 for a win, -1 for a loss, or zero for a push/unfinished hit. An episode is one complete hand. A policy chooses actions. V(s) estimates a state's return; Q(s,a) estimates return after taking a particular action and following the policy afterward. Neither is a win probability.

Our Foundations environment draws with replacement, the dealer stands on soft 17, and there is no natural bonus, splitting, or doubling. This learner does not apply unchanged to the planned six-deck public game.

## From prediction to control

TD prediction updated V while keeping the hit-below-17 rule fixed. SARSA updates Q, and its action choices respond to Q. It combines the exploration from Monte Carlo control with the one-step updates from TD.

The name records five items: **State, Action, Reward, next State, next Action**. The last action matters: SARSA uses the action its exploratory policy actually selected. This is called **on-policy** learning. In contrast, the Q-learning target introduced later uses the largest next action value, even when the next executed action is different.

Training uses epsilon-greedy choices: with probability epsilon choose uniformly between hit and stand; otherwise choose a highest-valued action (randomize ties). With epsilon 0.1 and a unique best action, that action is selected with probability 0.9 + 0.1/2 = 0.95. Exploration can select it too.

## Derive one update

Let Q(s,a) be the old estimate, r the reward, and a′ the action selected in next state s′. Gamma is 1 for these finite undiscounted hands. Alpha is the learning rate, here 0.1.

1. If the hand continues, target = r + gamma × Q(s′,a′).
2. If the hand ends, target = r. Do not select another action or bootstrap.
3. Error = target − Q(s,a).
4. New Q(s,a) = old Q(s,a) + alpha × error.

Example: old Q=0.2, reward=0, next stand Q=0.8, next hit Q=-0.4. Suppose exploration selects hit. SARSA's target is -0.4, error=-0.6, new Q=0.2 + 0.1×(-0.6)=**0.14**. Replacing the selected value with max(0.8,-0.4) would give 0.26 and would change the algorithm.

For a terminal loss instead, the target is -1 and the new estimate is 0.08. For a terminal push it is 0.18. The next observation may look like the current state after standing, but termination still removes all future value.

## Follow the code

Open [foundations/sarsa.py](../../foundations/sarsa.py).

1. `train` initializes empty Q/count dictionaries and separate environment/action random generators. Missing values start at zero.
2. After reset, choose the first action using the existing `epsilon_greedy` helper.
3. Execute it using `env.step(action)`.
4. If the hand continues, select `next_action` **once, before updating Q**. If terminal, use `None`.
5. `update` reads the selected next value, computes the target/error, and changes only the current state-action entry.
6. Increment the update count. It measures experience, not certainty.
7. Carry `state, action = next_state, next_action` forward. Resampling here would disconnect the target action from the executed action.
8. At termination, record the hand's outcome and start a new hand.

Unlike MC control, SARSA does not wait for the whole return. Unlike TD prediction, its estimates affect future actions. Constant alpha retains sampling fluctuations; constant epsilon retains exploration. This implementation is a teaching baseline, not a claim of convergence to an optimal strategy.

## Run the experiment

From the project root:

```sh
python3 -m foundations.sarsa --episodes 50000 --eval-episodes 20000 --seed 7 --eval-seed 1000007 --epsilon 0.1 --alpha 0.1 --trace --output /tmp/blackjack-sarsa.json
python3 -m unittest discover -s tests -v
```

The trace shows the first hand's numbers at update time. Early nonterminal targets may be zero because initialization is zero. Evaluation freezes Q and uses a greedy policy on a separate seed, with stand on ties. This differs from exploratory training behavior. Evaluation reuses the established [control evaluator](../../foundations/control.py), so it never updates Q.

The JSON is labelled `sarsa_control`; the policy-table renderer now accepts it with an explicit SARSA label and alpha. The state-value map remains incompatible. Unvisited actions export null and zero visits, although action selection uses their initial value zero.

Seed 7's preliminary frozen-greedy mean was -0.05540 over 20,000 evaluation hands; threshold was -0.08195 and random -0.38865. These are net reward units per hand. The approximate 95% interval for greedy was [-0.06859, -0.04221], reflecting evaluation sampling only, not variation in training. Equal evaluation seeds do not create identical hands across different policies. Several independent training seeds are needed before generalizing. Do not tune parameters on these results and then call the same evaluation a held-out test.

See [the daily record](../daily/2026-09-28.md) for verified checkpoints and limitations.

## Exercise

1. Old Q=-0.3, reward=0, selected next-action Q=0.5, alpha=0.2. Compute target, error, and new Q.
2. Repeat for a terminal win. Does the selected next-action estimate matter?
3. Next stand Q=0.7 and hit Q=-0.2, but exploration picks hit. Which value does SARSA use? What would Q-learning use?
4. Why must the implementation carry the selected next action into the next loop iteration?
5. Does frozen greedy evaluation measure exactly the same policy as exploratory SARSA training?

[Separate answers](solutions/05-sarsa.md). Next checkpoints will replicate unchanged settings across seeds and improve how the lesson can be inspected. Q-learning comes afterward.
