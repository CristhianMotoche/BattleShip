import abc
from dataclasses import dataclass
from typing import Any

from battlefield.game.domain.entities import (
    Player,
    PlayerAction,
    PlayerPhase,
    GameState,
)


class ResponderClient(abc.ABC):
    @abc.abstractmethod
    def send_to(self, other: Player, message: str) -> Any:
        pass


@dataclass
class Responder:
    action: PlayerAction
    player_status: PlayerPhase
    game: GameState
    client: ResponderClient

    def perform(self) -> Any:
        if self.action.is_placing():
            return self.client.send_to(self.game.opponent_player, "Placing")
        elif self.action.is_ready():
            return self.client.send_to(self.game.opponent_player, "Ready")
        elif self.action.is_playing():
            return self.client.send_to(self.game.opponent_player, "Playing")
        return self.client.send_to(self.game.current_player, "Invalid action")
