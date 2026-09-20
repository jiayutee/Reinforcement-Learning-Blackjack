# Lesson 1: a player interacting with an environment

Goal: run a blackjack player, explain every part of a transition, and change one decision rule. You need Python 3.9 or newer. This lesson uses only Python's standard library; the old prototype's dependencies are not required.

## 1. Run the example

In a terminal, enter the project folder and run:

```sh
python3 -m foundations.play --seed 7 --episodes 3
```

`-m` runs a Python module inside the project. `--episodes 3` plays three complete hands. `--seed 7` fixes the initial random-generator state, so rerunning this command reproduces the same experiment in the same Python environment. Changing the seed changes the sampled games.

Read code in this order: `score_hand` in `foundations/blackjack.py`, `reset`, `step`, then the loop in `foundations/play.py`. You do not need to understand neural networks or the old prototype yet.

## 2. The smallest RL vocabulary

The **agent** chooses an action. The **environment** applies the rules and returns feedback. An **episode** is one complete hand, from dealing to settlement.

| Term | Meaning in this lesson |
|---|---|
| Observation | `(player total, dealer upcard, usable ace)` |
| Action | `0` = stand, `1` = hit |
| Reward | `+1` win, `-1` loss, `0` push or unfinished hand |
| Policy | A rule for choosing an action from the observation |
| Return | Sum of rewards over the episode, with no discount here |
| Terminal | The hand has ended; the next hand requires `reset()` |

The environment's full state includes the hidden dealer card. The agent's observation excludes it. A usable ace is an ace currently counted as 11 without busting. An ace shown by the dealer is encoded as `1`.

The random policy picks each action with probability one half. It does **not learn**. It is our baseline and lets us check the environment before trusting a learning algorithm.

## 3. Work through one transition

Suppose you hold a 10 and a 6, and the dealer shows a 10. The observation is `(16, 10, False)`.

You hit and draw a 3:

```text
observation       action   next observation   reward   done
(16, 10, False)   hit      (19, 10, False)     0        False
```

Then you stand. Suppose the dealer finishes at 18. The reward is `+1` and `done=True`. Your return is `0 + 1 = 1`. That earlier zero did not mean hitting was bad: it meant the outcome had not arrived yet. Learning how to assign later outcomes to earlier decisions is a central RL problem.

`done` matters: zero reward can also be a terminal push. Reward alone does not tell us whether to continue.

## 4. Understand the code

```python
observation = env.reset()
done = False
while not done:
    action = choose_action(observation)
    next_observation, reward, done = env.step(action)
    observation = next_observation
```

This is pseudocode for the actual loop; `choose_action` stands for the policy logic in `play.py`. A `while` loop repeats until its condition becomes false. A tuple groups several values; `observation[0]` reads its first item, the player's total. `step` returns three values, which Python assigns to three variable names.

`score_hand` first counts every ace as 1. If adding 10 would keep the total at most 21, it promotes one ace to 11. Two aces cannot both count as 11 without busting.

The environment and agent have separate random generators. Changing how often the agent samples random actions therefore does not directly consume the environment's random numbers. Different actions can still change how many cards are drawn, so the same seed is not a guarantee of identical hands across different policies.

## 5. The rules are intentionally simple

Cards are drawn with replacement. Each of thirteen ranks is equally likely, so a ten-valued card has probability `4/13`, not `1/10`. The dealer stands on all totals of 17 or more, including soft 17. Players can only hit or stand. Two-card 21 receives no bonus and ties with dealer multi-card 21.

These are the planned Foundations rules, corresponding to the reward/rule settings `natural=False, sab=False` of [Gymnasium Blackjack](https://gymnasium.farama.org/environments/toy_text/blackjack/). This implementation is plain Python, not a Gymnasium environment or a claimed bit-for-bit replica. Cross-library statistical validation is still pending. The realistic web game will have its own explicitly versioned rules.

## 6. Your first experiment

Run both policies:

```sh
python3 -m foundations.play --policy random --episodes 10000 --quiet
python3 -m foundations.play --policy threshold --episodes 10000 --quiet
```

The threshold policy hits below 17 and stands otherwise. It is also fixed, not learned or an optimal blackjack strategy.

Mean return is `(wins - losses) / number_of_hands` under these unit payouts. For example, 40 wins, 50 losses, and 10 pushes means a return of `-0.10` units per hand. It is not a prediction of the next hand. Repeat with other seeds before drawing conclusions; formal uncertainty estimates arrive in the evaluation lesson.

Exercise: find `observation[0] < 17` in `foundations/play.py`, change 17 to 18, and predict the tradeoff before running it. You will sometimes improve your total and sometimes bust more often. Record both the seed and the threshold. Restore 17 afterward to keep the baseline reproducible.

## 7. Check your understanding

1. Why is the hidden dealer card absent from the observation?
2. What is the difference between reward and return?
3. Does `reward=0` mean the hand ended?
4. What does a seed make reproducible, and what does it not establish?
5. Why is the random player not a reinforcement learning agent yet?

Write your answers before opening [the worked answers](solutions/01-agent-environment.md).

Next lesson: estimate how good a policy is by averaging completed-hand returns (Monte Carlo prediction). After that, use estimated action values to improve the policy.
