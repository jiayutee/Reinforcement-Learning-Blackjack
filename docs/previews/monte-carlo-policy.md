# Learned hit/stand table

A snapshot of one trained policy, not an optimal blackjack strategy or a win-probability chart.

Training: 50,000 hands, seed 7, epsilon 0.1.
Rules: replacement draws, dealer stands on soft 17, no natural bonus, hit/stand only.

`H` = hit; `S` = stand. Decisions use the greater estimated Q; ties prefer stand.
`*` = at least one action has fewer than 20 visits. This is a count warning, not a confidence interval.
`?` = at least one action has never been tried; no evidence-backed comparison is shown. The actual evaluator still uses zero initialization for missing estimates.
`—` = no observed decision at that position; some cells represent impossible hands. None of these marks means zero value.

## Hard hands: no usable ace

| Your total / dealer | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S` |
| 20 | `S` | `S*` | `S` | `S` | `S` | `S` | `S` | `S` | `S` | `S` |
| 19 | `S` | `S*` | `S*` | `S*` | `S*` | `S*` | `S` | `S*` | `S` | `S` |
| 18 | `S` | `S*` | `S*` | `S*` | `S` | `S` | `S*` | `S*` | `S` | `S` |
| 17 | `S` | `S*` | `S` | `S*` | `S` | `S*` | `S` | `S` | `S*` | `S` |
| 16 | `H` | `S*` | `S` | `S` | `S` | `S` | `H` | `S` | `S` | `S` |
| 15 | `S` | `S` | `S` | `S` | `S` | `S` | `S` | `S` | `H` | `H` |
| 14 | `H` | `S` | `H` | `S` | `S*` | `S*` | `H*` | `S` | `H` | `H` |
| 13 | `H` | `S` | `H` | `S` | `S` | `H` | `H` | `H*` | `H` | `S` |
| 12 | `H` | `S` | `S` | `S` | `H` | `S` | `S` | `H` | `S` | `H` |
| 11 | `H*` | `H*` | `H*` | `H*` | `H` | `H` | `H*` | `H` | `H*` | `H` |
| 10 | `H*` | `H*` | `H*` | `H` | `H*` | `H` | `H*` | `H*` | `H` | `H` |
| 9 | `H` | `H` | `H` | `H*` | `H*` | `H` | `H*` | `H*` | `H` | `H` |
| 8 | `H*` | `H*` | `H*` | `H*` | `H*` | `S*` | `H*` | `H*` | `H*` | `H` |
| 7 | `S` | `H*` | `H*` | `H*` | `H` | `H*` | `H*` | `H` | `H*` | `H` |
| 6 | `H*` | `H*` | `H` | `H*` | `H*` | `H*` | `S*` | `H*` | `H` | `S*` |
| 5 | `H*` | `H*` | `S*` | `H*` | `H*` | `H*` | `S*` | `H*` | `H*` | `H` |
| 4 | `H*` | `S*` | `H*` | `H*` | `S*` | `H*` | `H*` | `H*` | `S*` | `S*` |

## Soft hands: a usable ace counts as 11

| Your total / dealer | A | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 21 | `S*` | `S` | `S*` | `S` | `S*` | `S*` | `S*` | `S*` | `S*` | `S` |
| 20 | `S*` | `S` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` |
| 19 | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `S*` | `H*` | `H*` | `S` |
| 18 | `H*` | `H*` | `S*` | `S*` | `H` | `S*` | `S*` | `H*` | `S*` | `S` |
| 17 | `S*` | `H*` | `S*` | `S*` | `S*` | `S*` | `S*` | `H*` | `S*` | `H*` |
| 16 | `H*` | `H*` | `S*` | `S*` | `H*` | `H*` | `H*` | `H*` | `H*` | `H` |
| 15 | `H` | `S*` | `S*` | `H*` | `H*` | `S*` | `H*` | `S*` | `H*` | `H*` |
| 14 | `H*` | `H*` | `S*` | `H*` | `S*` | `H*` | `S*` | `H*` | `H*` | `H*` |
| 13 | `H*` | `H*` | `H*` | `H*` | `H*` | `H` | `H*` | `H*` | `S*` | `H*` |
| 12 | `H*` | `H*` | `H*` | `H*` | `S*` | `H*` | `S*` | `H*` | `H*` | `S*` |
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
| (12, 6, False) | -0.15287 / 314 | -0.20619 / 97 | `S` |
| (16, 10, False) | -0.56989 / 837 | -0.58314 / 866 | `S` |
| (18, 9, True) | -0.10526 / 57 | -0.20000 / 5 | `S*` |
| (20, 10, False) | +0.43670 / 2038 | -0.80000 / 130 | `S` |

Data source commit: `4b93436ee3b28707febf9b2c0f099bd8b90177fb`. Foundations source dirty: `False`.

The count cutoff changes only the warning marks, not the estimates or policy. Even unmarked decisions can be noisy or wrong. Compare multiple training seeds before generalizing.
