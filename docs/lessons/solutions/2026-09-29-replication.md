# Replication exercise answers

1. -0.06055 - (-0.07725) = **+0.01670** reward units per hand.
2. No. It is a difference between two negative means. SARSA's mean is -0.06249; it lost reward on average in these samples.
3. That interval reflects sampled games for one fixed policy, not how different training experience changes the learned policy. Repeated training seeds address another source of variation.
4. No. This implementation reproduces the same training path with the same seed and settings. Repeating it verifies reproducibility, not independent training evidence.

## Policy table exercise

The warning considers **both** actions. Stand has only 138 updates, below 200, so the comparison receives an asterisk even though hit has 312. Raising the cutoff changes the annotation, not Q, training, or the greedy decision. This is a count warning, not a statistical confidence test.
