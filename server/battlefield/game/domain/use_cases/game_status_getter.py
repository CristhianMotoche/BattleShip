from dataclasses import dataclass, field
from typing import List

from battlefield.game.domain.entities import GameState, Player


@dataclass
class GameStatusGetter:
    players: List[Player] = field(default_factory=list)

    def perform(self) -> GameState:
        pass
