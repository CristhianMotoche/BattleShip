import abc
from dataclasses import dataclass

from battlefield.game.domain.entities import (
    Player,
    PlayerAction,
    PlayerPhase,
    GameState,
)


class ResponderClient(abc.ABC):
    @abc.abstractmethod
    def send_to(self, other: Player, message: str) -> None:
        pass


@dataclass
class Responder:
    action: PlayerAction
    player_status: PlayerPhase
    game: GameState
    client: ResponderClient

    def perform(self) -> None:
        if self.action.is_placing():
            self.client.send_to(self.game.opponent_player, "FOO")
