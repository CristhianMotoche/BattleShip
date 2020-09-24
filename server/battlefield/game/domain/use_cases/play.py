from dataclasses import dataclass
from typing import Any, List

from battlefield.game.domain.use_cases.responder import (
    Responder,
    ResponderClient,
)
from battlefield.game.domain.use_cases.updater import Updater
from battlefield.game.domain.use_cases.game_status_getter import (
    StatusGetter,
    NotEnoughPlayers,
    MoreThanExpected,
)

from ..entities import Game, Player, PlayerAction


@dataclass(frozen=True)
class Play:
    _game: Game
    _player: Player
    _action: PlayerAction
    _responder: ResponderClient

    def perform(self) -> Any:
        try:
            current_game = StatusGetter(self._game._players).perform()
        except (NotEnoughPlayers, MoreThanExpected):
            return self._responder.send_to(self._player, "Missing players")
        else:
            updated_player = Updater(
                current_game.current_player,
                self._action,
                current_game.get_status(),
            ).perform()
            update_player_in_list(
                self._game._players,
                current_game.current_player,
                updated_player,
            )
            return Responder(
                self._action, current_game, self._responder,
            ).perform()


def update_player_in_list(
    players: List[Player], old_player: Player, updated_player: Player
) -> None:
    players.remove(old_player)
    players.append(updated_player)
