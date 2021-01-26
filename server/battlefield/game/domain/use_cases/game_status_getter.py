from dataclasses import dataclass
from typing import List

from battlefield.game.domain.entities import GameState, Player


class NotEnoughPlayers(Exception):
    pass


class MoreThanExpected(Exception):
    pass


@dataclass
class StatusGetter:
    _players: List[Player]

    MAX_PLAYERS = 2

    def perform(self) -> GameState:
        if len(self._players) > self.MAX_PLAYERS:
            raise MoreThanExpected()

        if not self._players or len(self._players) <= 1:
            raise NotEnoughPlayers()

        return GameState(self._players[0], self._players[1])
