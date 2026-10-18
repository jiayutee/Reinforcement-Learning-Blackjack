"""First-visit Monte Carlo state-value prediction for collected rounds."""
from dataclasses import dataclass
from typing import Dict, Tuple


def state_key(observation):
    """Compact visible decision features; rule profile/stake are fixed per run."""
    index = observation['active_hand']
    hand = observation['hands'][index]
    return (hand['total'], hand['usable_ace'],
            observation['dealer'][0]['rank'], hand['from_split'],
            hand['split_aces'], len(observation['hands']),
            tuple(observation['legal_actions']))


@dataclass(frozen=True)
class Estimate:
    count: int
    value: float


class FirstVisitMonteCarlo:
    def __init__(self, gamma=1.0):
        if type(gamma) not in (int, float) or not 0 <= gamma <= 1:
            raise ValueError('gamma must be between zero and one')
        self.gamma = float(gamma)
        self._counts: Dict[Tuple, int] = {}
        self._values: Dict[Tuple, float] = {}
        self.episodes = 0
        self.decision_episodes = 0
        self.opening_terminals = 0

    @property
    def estimates(self):
        return {key: Estimate(self._counts[key], value)
                for key, value in self._values.items()}

    def update(self, episode):
        """Update V(s) from first occurrence returns; never update action values."""
        self.episodes += 1
        if not episode.transitions:
            self.opening_terminals += int(episode.opening_terminal)
            return
        self.decision_episodes += 1
        transitions = episode.transitions
        returns = [0.0] * len(transitions)
        running = 0.0
        for i in range(len(transitions)-1, -1, -1):
            running = transitions[i].reward + self.gamma * running
            returns[i] = running
        seen = set()
        for transition, target in zip(transitions, returns):
            key = state_key(transition.observation)
            if key in seen:
                continue
            seen.add(key)
            count = self._counts.get(key, 0) + 1
            old = self._values.get(key, 0.0)
            self._values[key] = old + (target - old) / count
            self._counts[key] = count
