"""Hand facts for public rules; settlement and legal actions remain engine duties."""
from dataclasses import dataclass
from typing import Sequence

from foundations.blackjack import score_hand
from public_game.cards import Card


@dataclass(frozen=True)
class HandFacts:
    total: int
    usable_ace: bool
    bust: bool
    natural: bool
    equal_rank_pair: bool


def hand_facts(cards: Sequence[Card], *, from_split: bool = False) -> HandFacts:
    if type(from_split) is not bool:
        raise ValueError('from_split must be a boolean')
    if not cards or any(not isinstance(card, Card) for card in cards):
        raise ValueError('Expected a nonempty sequence of Cards')
    total, usable = score_hand([card.value for card in cards])
    pair = len(cards) == 2 and cards[0].rank == cards[1].rank
    return HandFacts(total, usable, total > 21,
                     len(cards) == 2 and total == 21 and not from_split, pair)
