from dataclasses import dataclass

from battlefield.game.domain.entities import GameState


@dataclass
class Updater:

    data: str
    game: GameState

    def perform(self):
        pass
