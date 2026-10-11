"""Aggregate completed hands; caller commits the returned credit once."""
from dataclasses import dataclass
from typing import Tuple

from public_game.settlement import Settlement, settle_hand
from public_game.splitting import SplitHand


@dataclass(frozen=True)
class RoundSettlement:
    hands: Tuple[Settlement, ...]
    stake: int
    credit: int
    profit: int
    initial_stake: int

    @property
    def normalized_profit(self):
        return self.profit / self.initial_stake


def settle_round(hands, dealer, initial_stake):
    """Pure accounting for 1-4 completed hands; no draws or balance mutation.

    Completion flags and dealer progression remain engine responsibilities.
    All stakes must already have been debited before applying total credit.
    """
    if type(initial_stake) is not int or initial_stake <= 0 or initial_stake % 2:
        raise ValueError('initial stake must be positive even half-chip units')
    hands = tuple(hands)
    if not 1 <= len(hands) <= 4:
        raise ValueError('expected one through four completed hands')
    if any(not isinstance(h, SplitHand) or h.complete is not True for h in hands):
        raise ValueError('all hands must be complete')
    if any(type(h.stake) is not int or h.stake not in (initial_stake, 2*initial_stake)
           for h in hands):
        raise ValueError('each stake must equal the initial wager or its double')
    results = tuple(settle_hand(h.cards, dealer, h.stake, from_split=h.from_split)
                    for h in hands)
    return RoundSettlement(results, sum(r.stake for r in results),
                           sum(r.credit for r in results),
                           sum(r.profit for r in results), initial_stake)
