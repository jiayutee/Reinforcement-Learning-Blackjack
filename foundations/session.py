"""One in-memory Foundations game session; transport-independent teaching example."""
import argparse
import copy
import json

from foundations.blackjack import Blackjack, HIT, STAND


class GameSession:
    def __init__(self, seed=0):
        self._game = Blackjack(seed)
        self._revision = 0
        self._started = False
        self._last_command = None
        self._transitions = []
        self._reward = None

    def view(self):
        return {"revision": self._revision,
                "hand": self._game.visible_hand() if self._started else None,
                "reward": self._reward, "last_command": self._last_command,
                "transitions": copy.deepcopy(self._transitions)}

    def command(self, name, expected_revision):
        """Apply one valid command. Rejected requests leave game and revision intact.

        Revision is an optimistic concurrency check, not authentication. A future
        concurrent server must serialize this entire check-and-update operation.
        """
        if type(expected_revision) is not int or expected_revision != self._revision:
            raise ValueError("Stale or invalid revision; fetch the current view.")
        if name not in ("deal", "hit", "stand"):
            raise ValueError("Unknown command.")
        if name == "deal":
            if self._started and not self._game.visible_hand()["done"]:
                raise ValueError("Finish the active hand before dealing again.")
            self._game.reset()
            self._transitions = []
            self._started = True
            self._reward = None
        else:
            if not self._started or self._game.visible_hand()["done"]:
                raise ValueError("Deal a new hand before acting.")
            visible = self._game.visible_hand()
            before = [visible['player_total'], visible['dealer_cards'][0], visible['player_usable_ace']]
            action = HIT if name == "hit" else STAND
            observation, reward, done = self._game.step(action)
            self._transitions.append({'observation': before, 'action': action,
                                      'reward': reward, 'next_observation': list(observation),
                                      'done': done})
            self._reward = reward if done else None
        self._last_command = name
        self._revision += 1
        return self.view()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    session = GameSession(args.seed)
    print("Foundations teaching game: deal, hit, stand, quit. Values only; no suits or wagers.")
    while True:
        print(json.dumps(session.view()))
        try:
            command = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if command == "quit":
            break
        try:
            session.command(command, session.view()["revision"])
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()
