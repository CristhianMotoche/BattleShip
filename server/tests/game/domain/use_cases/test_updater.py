from unittest import TestCase

from battlefield.game.domain.entities import (
    Player,
    PlayerAction,
    PlayerPhase,
    GamePhase,
)
from battlefield.game.domain.use_cases.updater import Updater


class UpdaterUnitTest(TestCase):
    def test_updates_player_in_list_with_placing_state(self) -> None:
        p1 = Player(1, 1, None)
        expected = PlayerPhase.PLACING

        updated_player = Updater(
            p1, PlayerAction.PLACING, "", GamePhase.PLACING
        ).perform()

        assert updated_player.status == expected

    def test_updates_player_status_to_ready_when_game_is_placing(self) -> None:
        p1 = Player(1, 1, None)
        expected = PlayerPhase.READY

        updated_player = Updater(
            p1, PlayerAction.READY, "", GamePhase.PLACING
        ).perform()

        assert updated_player.status == expected

    def test_updates_player_status_to_ready_playing_when_game_is_ready(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        expected = PlayerPhase.PLAYING

        updated_player = Updater(
            p1, PlayerAction.PLAYING, "", GamePhase.READY
        ).perform()

        assert updated_player.status == expected

    def test_updates_player_status_to_attacking_when_game_is_playing(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        expected = PlayerPhase.ATTACKING

        updated_player = Updater(
            p1, PlayerAction.ATTACKING, "", GamePhase.PLAYING
        ).perform()

        assert updated_player.status == expected
