# Atomic transition answers

1. Nothing changes: revision stays 4, and balance, cards and randomness are preserved. The request is stale.
2. A tentative reshuffle consumes randomness. Preserving only cards could make a later reshuffle differ after a failed request. The failed command must not advance the authoritative random stream.
3. Revision 0 refers to an already accepted command and is rejected. A new request at revision 1 explicitly starts a new round, debits a new wager and can produce another payout. Repeated reads do neither.

## Hit/stand accounting

An ordinary win credits 2×20=40 units, making final balance 180+40=220. Net profit is 220-200=20. The credit includes the stake that was previously debited.

## Double accounting

You lose 20 chips in total, including the original 10 and additional 10. Normalized reward is -20/10=-2. The original stake is not subtracted a third time at settlement.
