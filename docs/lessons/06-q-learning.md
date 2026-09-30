# Lesson 6: Q-learning separates exploration from its target

## Prerequisites

Use Python 3.9+, loops, functions, dictionaries and arithmetic. Review [SARSA](05-sarsa.md) and [TD prediction](04-temporal-difference-prediction.md) if needed. A state is `(player total, dealer upcard, usable ace)`. An action is stand (0) or hit (1). Reward is +1 for a win, -1 for a loss, zero for a push or an unfinished hit. Q(s,a) estimates return after an action; it is not a win probability. An episode is a complete hand.

We still use replacement draws, dealer stands on soft 17, no natural bonus, hit/stand only. This is not the planned six-deck public game.

## Intuition: two action rules

The **behavior policy** generates experience. Here it is epsilon-greedy: usually choose a highest-valued action, sometimes choose randomly. The **target policy** is the greedy continuation represented by the largest next Q estimate. Q-learning is off-policy because these rules can differ.

SARSA uses the next action it actually selected. Q-learning uses the highest next estimate, even when exploration later chooses something else. Off-policy does not mean learning without an environment or without exploration. It describes the relationship between behavior and the learning target.

## Equations step by step

Let r be the reward, s′ the next observation, alpha the learning rate, and gamma the discount factor (1 here).

1. Unfinished hand: bootstrap = max(Q(s′,stand), Q(s′,hit)).
2. Target = r + gamma × bootstrap.
3. Terminal hand: replace that entire target with r. There is no next decision.
4. Error = target - Q(s,a).
5. New Q(s,a) = old Q(s,a) + alpha × error.

Worked example: old Q=0.2, r=0, next stand Q=0.8, next hit Q=-0.4, alpha=0.1.

- Maximum next estimate = 0.8.
- Target = 0 + 1×0.8 = 0.8.
- Error = 0.8-0.2 = 0.6.
- New Q = 0.2+0.1×0.6 = **0.26**.

If exploration picks hit next, SARSA would instead target -0.4 and produce **0.14**. Q-learning still produces 0.26. A terminal loss targets -1 and produces **0.08** for either method. A terminal push targets zero, regardless of the returned observation's stored Q values.

The maximum is over current estimates, which can be wrong. Selecting a maximum among noisy estimates can also introduce overestimation. Constant alpha and epsilon here do not satisfy all conditions needed for textbook convergence guarantees. This is a transparent baseline, not a guarantee of optimal play.

## Follow the code

Open [foundations/q_learning.py](../../foundations/q_learning.py), then compare with [SARSA](../../foundations/sarsa.py).

1. `train` creates empty Q/count dictionaries and separate seeded environment/action generators. Unknown Q starts at zero.
2. At each loop iteration, `epsilon_greedy` selects the behavior action using the current table.
3. The environment returns next state, reward and termination.
4. `update` reads both next-action estimates and uses `max` unless terminal. Only the current state-action entry changes.
5. Move to the next state and choose the next behavior action after the update. Unlike SARSA, no preselected next action needs to be carried forward.
6. Counts measure updates, not independent evidence or accuracy. Constant-alpha Q is not an arithmetic sample mean.
7. The first-hand trace records old value, bootstrap, target, error and updated value at the moment each update occurs.

The small training loop remains explicit beside SARSA so you can compare their timing. Both reuse the same environment, exploration helper and frozen evaluator; no generic algorithm framework is needed for this lesson.

Zero initialization deserves attention: if one next action has Q=-0.5 and another is unvisited, the maximum is zero. That is an initialization convention, not evidence that the unvisited action is safe. Exports preserve unvisited estimates as null with zero count.

## Run and interpret

```sh
python3 -m foundations.q_learning --episodes 50000 --eval-episodes 20000 --seed 7 --eval-seed 1000007 --epsilon 0.1 --alpha 0.1 --trace --output /tmp/blackjack-q-learning.json
python3 -m unittest discover -s tests -v
```

Evaluation freezes Q, removes exploration and uses a separate environment seed; ties prefer stand. It shares the established evaluator with SARSA and MC. The export is `q_learning_control`; the policy-table renderer accepts that type with an explicit Q-learning label and validates its alpha. State-value exports remain separate.

First seed-7 run: greedy mean **-0.08295** over 20,000 evaluation hands, approximate interval [-0.09615, -0.06975]; threshold -0.08195; random -0.38865. The greedy-minus-threshold difference is -0.00100 in this sample. This is not an established performance difference. The interval reflects evaluation game sampling only, not training variability. Equal seeds across policies do not guarantee identical hands, and these evaluation seeds have appeared in earlier experiments.

Do not conclude Q-learning is better because it uses a maximum, or worse because this one run trails a prior SARSA run. Repeat fixed settings across training seeds before comparing. See [today's record](../daily/2026-09-30.md).

## Exercise

1. Old Q=-0.3, next stand Q=0.2, next hit Q=-0.6, reward=0, alpha=0.2. Compute the Q-learning target and update.
2. If behavior next selects hit, what would SARSA's update be?
3. Repeat question 1 for a terminal win. Why is the maximum irrelevant?
4. One next action is unvisited and the other has Q=-0.5. What target does this implementation use with reward zero, and why is that not a quality guarantee?
5. Why must evaluation stop updating the learned table?

[Separate answers](solutions/06-q-learning.md). Next: replicate unchanged settings across seeds and make algorithm-labelled policy evidence available for inspection.
