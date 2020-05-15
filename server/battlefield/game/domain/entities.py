from dataclasses import dataclass
from typing import Any, NamedTuple, Optional
from enum import IntEnum, unique

from quart.wrappers import Websocket


@unique
class PlayerPhase(IntEnum):
    PLACING = 1
    READY = 2
    PLAYING = 3


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

    @classmethod
    def from_str(cls, string: str) -> Any:  # noqa
        return cls.PLACING


class Player(NamedTuple):
    id_: int
    session: int
    ws: Optional[Websocket]  # Optional just for unit tests
    status: PlayerPhase = PlayerPhase.PLACING
    turn: Optional[Turn] = None


@dataclass
class GameState:
    current_player: Player
    opponent_player: Optional[Player] = None
