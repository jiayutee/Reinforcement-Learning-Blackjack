"""Pure settlement arithmetic for a completed public-rule hand, in half-chip units."""
from dataclasses import dataclass
from typing import Sequence
from public_game.cards import Card
from public_game.hands import hand_facts


@dataclass(frozen=True)
class Settlement:
    outcome: str
    stake: int
    credit: int
    profit: int


def settle_hand(player: Sequence[Card], dealer: Sequence[Card], stake: int,
                *, from_split: bool = False) -> Settlement:
    """Stake is already debited. Caller owns phase, legality and one-time crediting.

    Whole-chip stakes are positive even half-chip integers. This function cannot
    infer whether the player stood; never call it to settle an active hand.
    """
    if type(stake) is not int or stake <= 0 or stake % 2:
        raise ValueError('stake must be positive even half-chip units')
    if len(player) < 2 or len(dealer) < 2:
        raise ValueError('Settlement requires at least two cards in each hand')
    p, d = hand_facts(player, from_split=from_split), hand_facts(dealer)
    if p.bust:
        outcome, credit = 'loss', 0
    elif d.natural:
        outcome, credit = ('push', stake) if p.natural else ('loss', 0)
    elif p.natural:
        outcome, credit = 'natural', 5 * stake // 2
    else:
        if not d.bust and d.total < 17:
            raise ValueError('Dealer must finish drawing before ordinary comparison')
        if d.bust or p.total > d.total:
            outcome, credit = 'win', 2 * stake
        elif p.total == d.total:
            outcome, credit = 'push', stake
        else:
            outcome, credit = 'loss', 0
    return Settlement(outcome, stake, credit, credit - stake)
