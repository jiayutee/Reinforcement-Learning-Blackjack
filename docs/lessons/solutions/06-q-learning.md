# Lesson 6 answers

1. Target=0.2; error=0.5; new Q=-0.3+0.2×0.5=**-0.2**.
2. SARSA uses selected hit Q=-0.6; error=-0.3; new Q=-0.3+0.2×(-0.3)=**-0.36**.
3. Target=1; error=1.3; new Q=**-0.04**. The hand ended, so no future action value belongs in the target.
4. Target=max(-0.5,0)=**0**. Zero is initialization for an unvisited action, not an observed expected return or evidence that it avoids losses.
5. Otherwise the policy changes during measurement, mixing learning with evaluation. A frozen policy makes the reported evaluation describe one fixed decision rule; it still leaves game-sampling uncertainty and training-seed variation.
