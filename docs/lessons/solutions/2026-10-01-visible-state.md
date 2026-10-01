# Visible-state exercise answers

1. The browser has the value in its data, regardless of what it draws. The environment must withhold it until reveal.
2. A total can disclose information about the hidden card even if the card list is masked.
3. Only the detached returned list changes. The environment keeps its own cards. A fresh view shows the original hand.
4. No. The player's bust already ended this hand; the dealer does not draw. This preview reveals the dealer's existing cards on any terminal outcome.

## Round control

Retrying with revision 2 would create a new valid command, drawing an additional card for a duplicated intention. Fetch and display the current state instead; the player can then choose a new action. The server needs atomic handling when concurrency is introduced.

`None` means no completed result is available. Zero means a completed push when the session's hand is done. The underlying RL environment also returns zero for unfinished hits, but the session deliberately keeps the final-result field unset until termination.
