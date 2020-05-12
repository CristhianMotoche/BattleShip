from dataclasses import dataclass
from typing import NamedTuple, Optional
from enum import IntEnum, unique


@unique
class PlayerPhase(IntEnum):
    PLACING = 1
    READY = 2
    PLAYING = 3


@unique
class Turn(IntEnum):
    Ours = 1
    Theirs = 2


class Player(NamedTuple):
    id_: int
    session: int
    status: PlayerPhase = PlayerPhase.PLACING
    turn: Optional[Turn] = None


@dataclass
class GameState:
    player_one: Player
    player_two: Player
