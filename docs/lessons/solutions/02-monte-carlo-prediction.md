# Lesson 2 worked answers

1. The counts and values are: `(1, 1)`, `(2, 0)`, `(3, 0)`, `(4, 0.25)`. The final value is `(1 - 1 + 0 + 1)/4 = 0.25`. A zero-return push still increments the count.
2. It was not observed as a decision state in this run. Its value is unknown to this estimator. Absence does not establish zero value, impossibility, or a recommended action.
3. The state-value table changes as experience arrives. The threshold rule choosing hit/stand never reads that table, so it remains unchanged. Prediction learns what to expect; control learns how to act.
4. A Monte Carlo target is the actual remaining return. Until the episode ends we do not know all the future rewards. A later method, temporal-difference learning, will use estimates to update before the episode ends.
5. Use the return from its earliest chronological occurrence, once per episode. Compute returns backward, then choose first visits forward. In an artificial episode `A --reward 1--> B --reward 2--> A --reward 3--> terminal`, update A with 6 and B with 5. Updating A with 3 would be a last-visit update.
6. In the `for state in [...]` display loop in `foundations/monte_carlo.py`, add `(18, 6, False)`. Run with `--output /tmp/blackjack-values.json` and locate the JSON observation `[18, 6, false]`. JSON uses lowercase `false`; Python uses `False`. Compare the count exactly and the value rounded to four decimal places. This display edit should not change any outcome or value estimate; the source-dirty provenance flag should become true until you commit it.

The example with repeated A is an algorithm test, not a claimed blackjack hand. It uses intermediate rewards to make first-visit versus last-visit behavior unmistakable.
