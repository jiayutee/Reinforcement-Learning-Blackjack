# Atomic transition answers

1. Nothing changes: revision stays 4, and balance, cards and randomness are preserved. The request is stale.
2. A tentative reshuffle consumes randomness. Preserving only cards could make a later reshuffle differ after a failed request. The failed command must not advance the authoritative random stream.
3. Revision 0 refers to an already accepted command and is rejected. A new request at revision 1 explicitly starts a new round, debits a new wager and can produce another payout. Repeated reads do neither.
