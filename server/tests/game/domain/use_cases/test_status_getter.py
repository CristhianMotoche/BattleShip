from unittest import TestCase

from battlefield.game.domain.entities import Player
from battlefield.game.domain.use_cases.game_status_getter import (
    StatusGetter,
    MoreThanExpected,
    NotEnoughPlayers,
)


class GameStatusGetterUnitTest(TestCase):
    def test_perform_raises_exception_when_player_list_is_empty(self) -> None:
        with self.assertRaises(NotEnoughPlayers):
            StatusGetter([]).perform()

    def test_perform_raises_exception_when_only_one_player_in_list(
        self,
    ) -> None:
        p1 = Player(1, 1, None)

        with self.assertRaises(NotEnoughPlayers):
            StatusGetter([p1]).perform()

    def test_perform_returns_game_status_with_players(self) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)

        game = StatusGetter([p1, p2]).perform()

        assert game.current_player is p1
        assert game.opponent_player is p2

    def test_perform_raises_exception_when_more_than_expected(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)
        p3 = Player(3, 1, None)

        with self.assertRaises(MoreThanExpected):
            StatusGetter([p1, p2, p3]).perform()
