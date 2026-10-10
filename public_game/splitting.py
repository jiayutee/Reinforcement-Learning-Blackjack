"""Pure split construction; session integration and shoe transactions are pending."""
from dataclasses import dataclass
from typing import Tuple

from public_game.cards import Card
from public_game.hands import hand_facts
from public_game.opening import validate_wager


@dataclass(frozen=True)
class SplitHand:
    cards: Tuple[Card, ...]
    stake: int
    from_split: bool
    split_aces: bool
    complete: bool


def split_hand(cards, additions, stake, balance, hand_count, *, split_aces=False):
    """Return two new hands and remaining balance; never draw or mutate inputs.

    Caller must establish active phase, revision and transaction before drawing
    the two additions. hand_count includes the hand being replaced. A previously
    split ace hand is ineligible, even if its one new card is another ace.
    """
    validate_wager(balance, stake)
    if type(hand_count) is not int or not 1 <= hand_count < 4:
        raise ValueError('split must leave at most four hands')
    if type(split_aces) is not bool or split_aces:
        raise ValueError('split aces cannot be resplit')
    original, added = tuple(cards), tuple(additions)
    if not hand_facts(original).equal_rank_pair:
        raise ValueError('split requires an equal-rank two-card pair')
    if len(added) != 2 or any(not isinstance(c, Card) for c in added):
        raise ValueError('split requires two added Cards in hand order')
    aces = original[0].rank == 'A'
    hands = tuple(SplitHand((original[i], added[i]), stake, True, aces,
                            aces or hand_facts((original[i], added[i])).total == 21)
                  for i in range(2))
    return hands, balance - stake
