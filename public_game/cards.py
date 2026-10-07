"""Finite rank/suit shoe, kept separate from the replacement-draw benchmark."""
from dataclasses import dataclass
import math
import random

RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
SUITS = ('clubs', 'diamonds', 'hearts', 'spades')
# Conservative bound for one player, <=4 final hands, automatic stop at 21, S17.
PUBLIC_ROUND_RESERVE = 4 * 21 + 17


@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        if self.rank not in RANKS or self.suit not in SUITS:
            raise ValueError('Invalid card rank or suit.')

    @property
    def value(self):
        # Ace promotion to 11 belongs to hand scoring, not individual cards.
        return 1 if self.rank == 'A' else 10 if self.rank in ('J', 'Q', 'K') else int(self.rank)


class Shoe:
    def __init__(self, decks=6, seed=0, penetration=0.75):
        if type(decks) is not int or not 1 <= decks <= 8:
            raise ValueError('decks must be an integer from 1 through 8')
        if type(penetration) not in (int, float) or not math.isfinite(penetration) or not 0 < penetration < 1:
            raise ValueError('penetration must be finite and between zero and one')
        self.decks = decks
        self.penetration = penetration
        self._rng = random.Random(seed)
        self._cards = []
        self._rebuild()

    def _rebuild(self):
        self._cards = [Card(rank, suit) for _ in range(self.decks) for suit in SUITS for rank in RANKS]
        self._rng.shuffle(self._cards)

    @property
    def remaining(self):
        return len(self._cards)

    @property
    def needs_shuffle(self):
        return (52 * self.decks - self.remaining) / (52 * self.decks) >= self.penetration

    def prepare_round(self, minimum_cards=0):
        """Caller must invoke only between rounds. Return whether a rebuild occurred.

        This primitive does not know round state; the future engine must enforce
        this boundary. There is no automatic shuffle during draw().
        """
        if type(minimum_cards) is not int or not 0 <= minimum_cards <= 52 * self.decks:
            raise ValueError('minimum_cards must fit within a full shoe')
        if self.needs_shuffle or self.remaining < minimum_cards:
            self._rebuild()
            return True
        return False

    def draw(self):
        if not self._cards:
            raise RuntimeError('Shoe exhausted; no mid-round reshuffle is allowed.')
        return self._cards.pop()
