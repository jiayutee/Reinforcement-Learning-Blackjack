"""Transactional public rounds; local single-threaded engine, no browser adapter."""
from copy import deepcopy
from dataclasses import dataclass, replace
from typing import Tuple, Optional

from public_game.cards import Card, Shoe, PUBLIC_ROUND_RESERVE
from public_game.hands import hand_facts
from public_game.opening import opening_round, validate_wager
from public_game.splitting import SplitHand, split_hand, validate_split
from public_game.round_settlement import RoundSettlement, settle_round


@dataclass(frozen=True)
class RoundState:
    hands: Tuple[SplitHand, ...]
    dealer: Tuple[Card, ...]
    initial_stake: int
    active: Optional[int]
    settlement: Optional[RoundSettlement]

    @property
    def phase(self):
        return 'settled' if self.settlement is not None else 'player_turn'


class PublicSession:
    def __init__(self, balance=200, seed=0):
        if type(balance) is not int or balance < 0:
            raise ValueError('balance must be nonnegative integer half-chip units')
        self._state = (Shoe(seed=seed), balance, 0, None)

    def deal(self, stake, expected_revision):
        shoe, balance, revision, previous = self._state
        if type(expected_revision) is not int or expected_revision != revision:
            raise ValueError('stale or invalid revision')
        if previous is not None and previous.phase != 'settled':
            raise ValueError('finish the current round before dealing')
        validate_wager(balance, stake)
        candidate = deepcopy(shoe)
        candidate.prepare_round(PUBLIC_ROUND_RESERVE)
        opening = opening_round([candidate.draw() for _ in range(4)], balance, stake)
        complete = opening.settlement is not None
        hands = (SplitHand(opening.player, stake, False, False, complete),)
        settlement = settle_round(hands, opening.dealer, stake) if complete else None
        result = RoundState(hands, opening.dealer, stake, None if complete else 0, settlement)
        self._state = (candidate, opening.balance, revision + 1, result)
        return self.view()

    def act(self, action, expected_revision):
        shoe, balance, revision, previous = self._state
        if type(expected_revision) is not int or expected_revision != revision:
            raise ValueError('stale or invalid revision')
        if previous is None or previous.phase != 'player_turn':
            raise ValueError('no active player hand')
        if action not in self.legal_actions():
            raise ValueError('action is not legal in the current state')
        candidate = deepcopy(shoe)
        hands = list(previous.hands)
        index = previous.active
        hand = hands[index]
        if action == 'split':
            # Eligibility was checked before drawing by legal_actions().
            children, balance = split_hand(hand.cards, (candidate.draw(), candidate.draw()),
                                           hand.stake, balance, len(hands),
                                           split_aces=hand.split_aces)
            hands[index:index+1] = children
        else:
            stake, player = hand.stake, hand.cards
            if action == 'double':
                balance -= stake
                stake *= 2
            if action in ('hit', 'double'):
                player += (candidate.draw(),)
            complete = action in ('stand', 'double') or hand_facts(player).total >= 21
            hands[index] = replace(hand, cards=player, stake=stake, complete=complete)
        active = next((i for i, h in enumerate(hands) if not h.complete), None)
        dealer, settlement = previous.dealer, None
        if active is None:
            if any(not hand_facts(h.cards).bust for h in hands):
                while hand_facts(dealer).total < 17:
                    dealer += (candidate.draw(),)
            settlement = settle_round(hands, dealer, previous.initial_stake)
            balance += settlement.credit
        result = RoundState(tuple(hands), dealer, previous.initial_stake, active, settlement)
        self._state = (candidate, balance, revision + 1, result)
        return self.view()

    def legal_actions(self):
        _, balance, _, result = self._state
        if result is None or result.phase != 'player_turn':
            return []
        hand = result.hands[result.active]
        actions = ['hit', 'stand']
        if len(hand.cards) == 2 and balance >= hand.stake and not hand.split_aces:
            actions.append('double')
        try:
            validate_split(hand.cards, hand.stake, balance, len(result.hands),
                           split_aces=hand.split_aces)
        except ValueError:
            pass
        else:
            actions.append('split')
        return actions

    def view(self):
        _, balance, revision, result = self._state
        def card(c):
            return {'rank': c.rank, 'suit': c.suit}
        settled = result is not None and result.phase == 'settled'
        selected = result.hands[result.active if result.active is not None else 0] if result else None
        settlements = result.settlement.hands if settled else ()
        return {
            'phase': result.phase if result else 'ready',
            'revision': revision, 'legal_actions': self.legal_actions(),
            'balance': balance,
            # Compatibility fields describe active hand, or first hand after settlement.
            'stake': selected.stake if selected else None,
            'player': [card(c) for c in selected.cards] if selected else [],
            'active_hand': result.active if result else None,
            'hands': [{'cards': [card(c) for c in h.cards], 'stake': h.stake,
                       'from_split': h.from_split, 'split_aces': h.split_aces,
                       'complete': h.complete,
                       'outcome': settlements[i].outcome if settled else None,
                       'profit': settlements[i].profit if settled else None}
                      for i, h in enumerate(result.hands)] if result else [],
            'initial_stake': result.initial_stake if result else None,
            'normalized_profit': result.settlement.normalized_profit if settled else None,
            'dealer': ([card(c) for c in result.dealer] if settled else
                       [card(result.dealer[0]), None] if result else []),
            'dealer_total': hand_facts(result.dealer).total if settled else None,
            'outcome': (settlements[0].outcome if len(settlements) == 1 else 'multiple') if settled else None,
            'profit': result.settlement.profit if settled else None,
        }
