from unittest import TestCase

from battlefield.game.domain.entities import Player
from battlefield.game.domain.use_cases.game_status_getter import (
    GameStatusGetter,
    MoreThanExpected,
    NotEnoughPlayers,
    PlayerNotFound,
)


class GameStatusGetterUnitTest(TestCase):
    def test_perform_raises_exception_when_player_list_is_empty(self) -> None:
        with self.assertRaises(NotEnoughPlayers):
            GameStatusGetter(1234, 1, []).perform()

    def test_perform_returns_game_state_when_list_only_has_one_player(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        game = GameStatusGetter(1, 1, [p1]).perform()

        assert game.current_player is p1
        assert game.opponent_player is None

    def test_perform_raises_exception_when_two_players_join(self) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)

        game = GameStatusGetter(1, 1, [p1, p2]).perform()

        assert game.current_player is p1
        assert game.opponent_player is p2

    def test_perform_raises_exception_when_current_player_not_found(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)

        with self.assertRaises(PlayerNotFound):
            GameStatusGetter(123, 1, [p1, p2]).perform()

    def test_perform_raises_exception_when_more_than_expected(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)
        p3 = Player(3, 1, None)

        with self.assertRaises(MoreThanExpected):
            GameStatusGetter(1, 1, [p1, p2, p3]).perform()
