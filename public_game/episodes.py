"""Collect one public-rule round from visible observations; no learning updates."""
from copy import deepcopy
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Transition:
    observation: dict
    action: str
    reward: float
    next_observation: dict
    done: bool


@dataclass(frozen=True)
class Episode:
    transitions: Tuple[Transition, ...]
    normalized_profit: float
    opening_terminal: bool


def collect_round(session, policy, stake=20):
    """Policy receives a detached visible snapshot and returns a legal action.

    Session/shoe persist between calls. Opening naturals are reported without a
    fictitious action. Exceptions propagate: earlier accepted actions remain
    accepted; this function does not roll back an entire episode.
    """
    view = session.deal(stake, session.view()['revision'])
    if view['phase'] == 'settled':
        return Episode((), view['normalized_profit'], True)
    transitions = []
    while view['phase'] == 'player_turn':
        action = policy(deepcopy(view))
        if action not in view['legal_actions']:
            raise ValueError('policy selected an illegal action')
        following = session.act(action, view['revision'])
        done = following['phase'] == 'settled'
        reward = following['normalized_profit'] if done else 0.0
        transitions.append(Transition(view, action, reward, following, done))
        view = following
    return Episode(tuple(transitions), view['normalized_profit'], False)
