# Policy review: worked answers

1. Random chooses hit or stand with probability 1/2 each, even at 20. Threshold-17 stands at 20. Neither of these policies uses the dealer upcard; the observation contains it, but these simple rules ignore it.
2. Value is `(-1 + 1 + 1 + 0)/4 = 0.25` units. Two of four hands won, so the sample win rate is `2/4 = 50%`. The push contributes zero reward but still counts in both denominators.
3. No. The current policy chooses by its fixed threshold; it does not consult the learned values. Changing decisions requires a policy-improvement step. Merely estimating a policy more accurately is prediction, not control.
4. A natural bonus changes rewards, and SAB rules change some natural outcomes. Different game settings produce different target values. A mismatch could look like a bug or a better agent when it is actually a different task.
