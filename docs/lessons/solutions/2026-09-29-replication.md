# Replication exercise answers

1. -0.06055 - (-0.07725) = **+0.01670** reward units per hand.
2. No. It is a difference between two negative means. SARSA's mean is -0.06249; it lost reward on average in these samples.
3. That interval reflects sampled games for one fixed policy, not how different training experience changes the learned policy. Repeated training seeds address another source of variation.
4. No. This implementation reproduces the same training path with the same seed and settings. Repeating it verifies reproducibility, not independent training evidence.
