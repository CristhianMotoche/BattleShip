import abc
from dataclasses import dataclass
from typing import List

from battlefield.game.domain.entities import GameState, Player


class NotEnoughPlayers(Exception):
    pass


class MoreThanExpected(Exception):
    pass


class GetterRepository(abc.ABC):
    @abc.abstractmethod
    def lookup_for_players(self, session_id: int) -> List[Player]:
        pass


@dataclass
class StatusGetter:
    session_id: int
    _repo: GetterRepository

    MAX_PLAYERS = 2

    def perform(self) -> GameState:
        players = self._repo.lookup_for_players(self.session_id)

        if len(players) > self.MAX_PLAYERS:
            raise MoreThanExpected

        if not players or len(players) <= 1:
            raise NotEnoughPlayers

        return GameState(players[0], players[1])
