from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Any, Dict, List, NamedTuple, Optional

from quart.wrappers import Websocket


@unique
class PlayerPhase(IntEnum):
    PLACING = 1
    READY = 2
    PLAYING = 3
    ATTACKING = 4


@unique
class Turn(IntEnum):
    Ours = 1
    Theirs = 2


@unique
class PlayerAction(IntEnum):
    PLACING = 1
    READY = 2
    PLAYING = 3
    ATTACKING = 4
    UNKNOWN = 5

    @classmethod
    def from_str(cls, string: str) -> Any:  # noqa
        if string == "Placing":
            return cls.PLACING
        elif string == "Ready":
            return cls.READY
        elif string == "Playing":
            return cls.PLAYING
        else:
            return cls.UNKNOWN

    def is_placing(self) -> bool:
        return self == self.PLACING

    def is_ready(self) -> bool:
        return self == self.READY

    def is_playing(self) -> bool:
        return self == self.PLAYING

    def is_attacking(self) -> bool:
        return self == self.ATTACKING


class Player(NamedTuple):
    id_: int
    session: int
    ws: Optional[Websocket]  # Optional just for unit tests
    status: PlayerPhase = PlayerPhase.PLACING
    turn: Optional[Turn] = None

    def set_placing(self) -> Any:
        return self.__set_phase(PlayerPhase.PLACING)

    def set_ready(self) -> Any:
        return self.__set_phase(PlayerPhase.READY)

    def set_playing(self) -> Any:
        return self.__set_phase(PlayerPhase.PLAYING)

    def set_attacking(self) -> Any:
        return self.__set_phase(PlayerPhase.ATTACKING)

    def __set_phase(self, phase: PlayerPhase) -> Any:
        dict_: Dict["str", Any] = {
            **self._asdict(),
            "status": phase,
        }
        return Player(**dict_)


@unique
class GamePhase(IntEnum):
    PLACING = 1
    READY = 2
    PLAYING = 3
    ATTACKING = 4

    def is_placing(self) -> bool:
        return self == self.PLACING

    def is_ready(self) -> bool:
        return self == self.READY

    def is_playing(self) -> bool:
        return self == self.PLAYING

    def is_attacking(self) -> bool:
        return self == self.ATTACKING


@dataclass
class GameState:
    current_player: Player
    opponent_player: Player

    def get_status(self) -> GamePhase:
        return GamePhase.PLACING


class Game:
    def __init__(self, session_id: int) -> None:
        self.session_id = session_id
        self._players: List[Player] = []
        self._turn = 0

    def append(self, player: Player) -> None:
        self._players.append(player)

    def remove(self, player: Player) -> None:
        self._players.remove(player)

    def get(self, player_id: int) -> Optional[Player]:
        return next(
            (player for player in self._players if player.id_ == player_id),
            None,
        )

    def __len__(self) -> int:
        return len(self._players)
