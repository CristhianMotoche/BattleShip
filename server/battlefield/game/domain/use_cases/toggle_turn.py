from typing import Dict, Any
from battlefield.game.domain.entities import Player, Turn


def toggle_turn(player: Player) -> Player:
    dict_: Dict["str", Any] = {
        **player._asdict(),
        "turn": next_turn(player.turn),
    }
    return Player(**dict_)


def next_turn(turn) -> Turn:
    if turn == Turn.Ours:
        return Turn.Theirs
    elif turn == Turn.Theirs:
        return Turn.Ours
    else:
        return turn
