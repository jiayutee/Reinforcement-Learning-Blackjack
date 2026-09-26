# Lesson 4 answers

1. Target = 0.2; error = 0.2 - (-0.4) = 0.6; new value = -0.4 + 0.25 * 0.6 = **-0.25**.
2. Terminal target = 0; error = 0.4; new value = **-0.3**. No future exists after the hand, even if the next observation has a stored estimate.
3. A stays 0 on its first update. B becomes -0.5. On the next A-to-B transition, A becomes 0 + 0.5 * (-0.5 - 0) = **-0.25**, assuming B has not changed again.
4. No. The policy still hits below 17 regardless of V. Prediction estimates a policy; control changes decisions. This lesson has no action-value comparison.
5. Few updates leave substantial sampling uncertainty, and bootstrapped targets can themselves be inaccurate. More visits help expose a state to experience but constant alpha retains fluctuations and gives recent targets more weight. Counts alone are not error bounds.

Changing alpha to 0.05 changes value updates but not the policy, environment draws, or game outcomes in this seeded implementation. Smaller alpha moves less on each step; it can be slower to adapt. This alone does not prove lower error.
