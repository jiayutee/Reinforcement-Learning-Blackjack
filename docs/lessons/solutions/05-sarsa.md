# Lesson 5 answers

1. Target=0.5; error=0.5-(-0.3)=0.8; new Q=-0.3+0.2×0.8=**-0.14**.
2. Terminal target=1; error=1.3; new Q=-0.3+0.2×1.3=**-0.04**. There is no next action after termination.
3. SARSA uses **-0.2**, the value of the selected hit. Q-learning uses **0.7**, the maximum next action value.
4. SARSA's target describes the chosen continuation. Resampling may execute a different continuation and violates the intended sampled SARSA sequence.
5. No. Training continues to explore; frozen greedy evaluation chooses only a maximal estimate and stands on ties. It measures the deployed greedy choice rule, not the exploratory behavior policy. Training noise and inaccurate Q estimates remain even after exploration is disabled.
