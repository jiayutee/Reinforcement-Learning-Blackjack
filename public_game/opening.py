"""Pure opening-deal transition; private engine state, never a browser payload."""
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from public_game.cards import Card
from public_game.hands import hand_facts
from public_game.settlement import Settlement, settle_hand


def validate_wager(balance: int, stake: int) -> None:
    """Call before preparing/drawing a shoe; balances may include half chips."""
    if type(balance) is not int or balance < 0:
        raise ValueError('balance must be nonnegative integer half-chip units')
    if type(stake) is not int or stake <= 0 or stake % 2 or stake > balance:
        raise ValueError('stake must be positive even half-chip units within balance')


@dataclass(frozen=True)
class OpeningRound:
    phase: str
    player: Tuple[Card, ...]
    dealer: Tuple[Card, ...]
    stake: int
    initial_stake: int
    balance: int
    settlement: Optional[Settlement]


def opening_round(dealt: Sequence[Card], balance: int, stake: int) -> OpeningRound:
    """Resolve four cards in player/dealer/player/dealer order without side effects.

    Balance is the PRE-deal balance. Naturals settle immediately; ordinary hands
    enter player_turn with their stake debited. The returned dealer includes the
    private hole card. A future session must own phase/revision validation,
    transactional shoe draws, visible snapshots and committing this result once.
    """
    validate_wager(balance, stake)
    cards = tuple(dealt)
    if len(cards) != 4 or any(not isinstance(card, Card) for card in cards):
        raise ValueError('opening requires exactly four Cards in deal order')
    player, dealer = (cards[0], cards[2]), (cards[1], cards[3])
    settlement = None
    if hand_facts(player).natural or hand_facts(dealer).natural:
        settlement = settle_hand(player, dealer, stake)
    return OpeningRound(
        phase='settled' if settlement is not None else 'player_turn',
        player=player, dealer=dealer, stake=stake, initial_stake=stake,
        balance=balance - stake + (settlement.credit if settlement else 0),
        settlement=settlement,
    )
