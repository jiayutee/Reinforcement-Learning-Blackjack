# Lesson 6 answers

1. Target=0.2; error=0.5; new Q=-0.3+0.2×0.5=**-0.2**.
2. SARSA uses selected hit Q=-0.6; error=-0.3; new Q=-0.3+0.2×(-0.3)=**-0.36**.
3. Target=1; error=1.3; new Q=**-0.04**. The hand ended, so no future action value belongs in the target.
4. Target=max(-0.5,0)=**0**. Zero is initialization for an unvisited action, not an observed expected return or evidence that it avoids losses.
5. Otherwise the policy changes during measurement, mixing learning with evaluation. A frozen policy makes the reported evaluation describe one fixed decision rule; it still leaves game-sampling uncertainty and training-seed variation.

## Replication exercise

Seed 42: -0.05755 - (-0.08205) = **+0.02450** reward units per hand. A relative improvement can still leave both policies with negative returns; the sampled Q-learning average is -0.06923. Expected profit is not established by these samples. Keeping unfavorable seeds avoids selecting only favorable evidence and exposes sensitivity to training/evaluation randomness.

## Policy evidence exercise

The cell changes from `S` to `S*`: stand has 97 updates, below 100. Both actions must meet the cutoff to avoid a warning. The action remains stand because the cutoff changes only presentation, not estimates or decisions. An unmarked cell is not a confidence guarantee.
