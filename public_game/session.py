"""Incremental public session: transactional deals only; not yet a playable game."""
from copy import deepcopy

from public_game.cards import Shoe, PUBLIC_ROUND_RESERVE
from public_game.hands import hand_facts
from public_game.opening import opening_round, validate_wager


class PublicSession:
    def __init__(self, balance=200, seed=0):
        if type(balance) is not int or balance < 0:
            raise ValueError('balance must be nonnegative integer half-chip units')
        # One authoritative bundle: shoe, balance, revision, opening result.
        self._state = (Shoe(seed=seed), balance, 0, None)

    def deal(self, stake, expected_revision):
        shoe, balance, revision, previous = self._state
        if type(expected_revision) is not int or expected_revision != revision:
            raise ValueError('stale or invalid revision')
        if previous is not None and previous.phase != 'settled':
            raise ValueError('finish the current round before dealing')
        validate_wager(balance, stake)
        # Copy includes RNG state. Failure discards all tentative draws/shuffles.
        candidate = deepcopy(shoe)
        candidate.prepare_round(PUBLIC_ROUND_RESERVE)
        result = opening_round([candidate.draw() for _ in range(4)], balance, stake)
        self._state = (candidate, result.balance, revision + 1, result)
        return self.view()

    def view(self):
        _, balance, revision, result = self._state
        def card(c):
            return {'rank': c.rank, 'suit': c.suit}
        settled = result is not None and result.phase == 'settled'
        return {
            'phase': result.phase if result else 'ready',
            'revision': revision,
            'balance': balance,
            'stake': result.stake if result else None,
            'player': [card(c) for c in result.player] if result else [],
            'dealer': ([card(result.dealer[0]),
                        card(result.dealer[1]) if settled else None] if result else []),
            'dealer_total': hand_facts(result.dealer).total if settled else None,
            'outcome': result.settlement.outcome if settled else None,
            'profit': result.settlement.profit if settled else None,
        }
