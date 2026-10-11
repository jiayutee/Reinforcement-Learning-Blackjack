# Round reward answers

Total stake=20+10+10=40 chips. Credits=0+20+10=30. Profit=30-40=-10. Normalize by initial wager10: -10/10=-1. Adding profit to an already-debited balance would charge stakes twice; add credit to return the appropriate stakes and winnings.

## Retry revisions

A failed command never commits, so the authoritative revision stays unchanged. A successful retry commits once and increments it. Replaying the old revision afterward is stale, preventing duplicate actions and payouts.
