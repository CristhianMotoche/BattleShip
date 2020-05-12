from dataclasses import dataclass, field
from typing import List

from battlefield.game.domain.entities import GameState, Player


class MoreThanExpected(Exception):
    pass


@dataclass
class GameStatusGetter:
    players: List[Player] = field(default_factory=list)

    def perform(self) -> GameState:
        if not self.players:
            return GameState()
        if len(self.players) == 1:
            return GameState(player_one=self.players[0])
        if len(self.players) == 2:
            return GameState(
                player_one=self.players[0], player_two=self.players[1]
            )
        raise MoreThanExpected()
