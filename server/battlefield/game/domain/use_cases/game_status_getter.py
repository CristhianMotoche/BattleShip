from dataclasses import dataclass
from typing import List

from battlefield.game.domain.entities import GameState, Player


class NotEnoughPlayers(Exception):
    pass


class MoreThanExpected(Exception):
    pass


class PlayerNotFound(Exception):
    pass


class WaitingPlayer(Exception):
    pass


@dataclass
class GameStatusGetter:
    player_id: int
    session_id: int
    players: List[Player]

    MAX_PLAYERS = 2

    def perform(self) -> GameState:
        if len(self.players) > self.MAX_PLAYERS:
            raise MoreThanExpected

        players_in_session = self.__look_up_in_session()

        if not players_in_session:
            raise NotEnoughPlayers

        current_player = self.__look_up_first_player(players_in_session)
        second_player = self.__look_up_second_player(players_in_session)

        return GameState(current_player, second_player)

    def __look_up_in_session(self) -> List[Player]:
        return list(
            filter(
                lambda player: player.session == self.session_id, self.players
            )
        )

    def __look_up_first_player(
        self, session_players: List[Player]
    ) -> Player:
        player = next(
            (
                player
                for player in session_players
                if player.id_ == self.player_id
            ),
            None,
        )
        if not player:
            raise PlayerNotFound()
        return player

    def __look_up_second_player(
        self, session_players: List[Player]
    ) -> Player:
        player = next(
            (
                player
                for player in session_players
                if player.id_ != self.player_id
            ),
            None,
        )
        if not player:
            raise WaitingPlayer()
        return player
