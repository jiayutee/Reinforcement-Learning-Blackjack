# Episode-trace answers

1. All three returns are -1: sum the remaining rewards from each decision onward. Immediate rewards differ from returns.
2. Standing can leave the player's total and dealer upcard unchanged, while the environment resolves the hand. The `done` flag specifies termination; observation equality does not.
3. No. The request was rejected before a transition occurred. Recording it would invent an action and distort the episode.
4. No. The session only records experience. A separate learning update would be required to change Q; frozen inference deliberately does not do that.
