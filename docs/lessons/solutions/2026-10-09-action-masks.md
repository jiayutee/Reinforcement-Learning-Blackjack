# Action mask answers

Stand is the greedy legal action. Double's larger value is irrelevant because it is unavailable.

With epsilon=0.2, stand probability is 0.8+0.2/2=0.9; hit probability is 0.2/2=0.1. At termination there is no future decision or bootstrap value: the target is the observed reward. Taking a maximum over an empty list is undefined and unnecessary.

## Independent random streams

Changing how many random choices the policy makes would also advance a shared shoe generator, changing later shuffles for an unrelated reason. Separate generators isolate those sources of randomness. This does not guarantee identical card exposure across policies: different actions still consume different numbers of cards.
