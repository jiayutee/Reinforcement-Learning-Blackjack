# Lesson 3 worked answers

1. Best action: `0.8 + 0.2/2 = 0.9`. Other action: `0.2/2 = 0.1`. With tied estimates, both actions get 0.5 in our training policy.
2. Increment the count to 5. New mean: `0.25 + (-1 - 0.25)/5 = 0`. Equivalently, the previous four samples sum to 1; adding -1 gives total 0 across five samples.
3. Hit, because -0.3 is greater than -0.5. Both estimates are negative, so this does not imply positive expected profit or a guaranteed win.
4. Evaluation should measure the behavior of one frozen policy on fresh outcomes. Updating during evaluation changes what is being measured and uses the evaluation games for learning.
5. Both missing estimates default to zero, and the deterministic evaluation tie rule selects stand. The export keeps missing estimates as null and zero visits, and evaluation reports unvisited selected actions. Zero initialization is not evidence about an untried action.
