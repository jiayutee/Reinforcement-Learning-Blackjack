# Settlement answers

1. Credit 20, profit 0. The returned stake is not profit.
2. Profit -40 units; normalized contribution -40/20=-2. A split round sums contributions from all hands before normalization by the initial stake.
3. A caller could add the same credit twice. The round engine must own settlement state and accept only one transition into settled status; rejected/repeated requests must not mutate balance.
