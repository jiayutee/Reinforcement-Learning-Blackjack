# Learned hit/stand table

A snapshot of one trained policy, not an optimal blackjack strategy or a win-probability chart.

Training: 50,000 hands, seed 7, epsilon 0.1.
Rules: replacement draws, dealer stands on soft 17, no natural bonus, hit/stand only.

`H` = hit; `S` = stand. Decisions use the greater estimated Q; ties prefer stand.
`*` = at least one action has fewer than 20 visits. This is a count warning, not a confidence interval.
`?` = at least one action has never been tried; no evidence-backed comparison is shown. The actual evaluator still uses zero initialization for missing estimates.
`—` = no observed decision at that position; some cells represent impossible hands. None of these marks means zero value.

Algorithm: one-step SARSA, constant alpha 0.1. Counts are updates; Q values are not sample means.
Training explores; this table shows frozen greedy choices. These estimates need not equal returns under the final greedy policy.

## Hard hands: no usable ace

| Your total / dealer | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S` |
| 20 | `S` | `S` | `S` | `S` | `S` | `S` | `S` | `S` | `S` | `S` |
| 19 | `S` | `S*` | `S` | `S*` | `S*` | `S*` | `S` | `S*` | `S` | `S` |
| 18 | `S` | `S` | `S` | `S` | `S` | `S*` | `S` | `S` | `S` | `S` |
| 17 | `S` | `H` | `S` | `S` | `S` | `S` | `S` | `S` | `S` | `S` |
| 16 | `H` | `S` | `S` | `S` | `H` | `S` | `H` | `S` | `S` | `H` |
| 15 | `H` | `H` | `S` | `S` | `H` | `S` | `H` | `H` | `H` | `S` |
| 14 | `H` | `H` | `S` | `S` | `S` | `S` | `H` | `H` | `H` | `H` |
| 13 | `H` | `S` | `S` | `H` | `S` | `S` | `H` | `H` | `H` | `H` |
| 12 | `H` | `H` | `H` | `S` | `H` | `H` | `H` | `H` | `H` | `H` |
| 11 | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` | `H` |
| 10 | `H*` | `H*` | `H*` | `H*` | `H` | `H*` | `H*` | `H*` | `H*` | `H` |
| 9 | `H*` | `H` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 8 | `H*` | `H` | `H*` | `H` | `H*` | `H` | `H*` | `H*` | `H*` | `H` |
| 7 | `H*` | `H*` | `H` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 6 | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 5 | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `S*` | `H*` | `H` |
| 4 | `H*` | `S*` | `H*` | `H*` | `H*` | `S*` | `H*` | `H*` | `H*` | `H*` |

## Soft hands: a usable ace counts as 11

| Your total / dealer | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S` | `S*` | `S` |
| 20 | `S` | `S*` | `S` | `H*` | `S*` | `S` | `S*` | `S*` | `S*` | `S*` |
| 19 | `S` | `S*` | `S*` | `S` | `S*` | `S*` | `S*` | `S*` | `S*` | `H` |
| 18 | `H*` | `S` | `S` | `H*` | `H` | `H*` | `S*` | `S*` | `H` | `H` |
| 17 | `S` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` | `H*` | `H` | `H` |
| 16 | `H*` | `H*` | `H*` | `H*` | `S*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 15 | `H*` | `H*` | `H*` | `H` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 14 | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 13 | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 12 | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H*` |
| 11 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |
| 10 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |
| 9 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |
| 8 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |
| 7 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |
| 6 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |
| 5 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |
| 4 | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` | `—` |

## Inspect the evidence

| State (total, dealer, usable ace) | Stand Q / visits | Hit Q / visits | Display |
|---|---|---|---|
| (12, 6, False) | -0.38702 / 138 | -0.36505 / 312 | `H` |
| (16, 10, False) | -0.81052 / 609 | -0.60227 / 1215 | `H` |
| (18, 9, True) | -0.35985 / 28 | -0.15835 / 44 | `H` |
| (20, 10, False) | +0.48902 / 2167 | -0.84304 / 112 | `S` |

Data source commit: `176a2ab4d6cb64995d2b166ed0f570da52df5cea`. Foundations source dirty: `False`.

The count cutoff changes only the warning marks, not the estimates or policy. Even unmarked decisions can be noisy or wrong. Compare multiple training seeds before generalizing.
