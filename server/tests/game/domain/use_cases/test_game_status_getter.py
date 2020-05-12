from unittest import TestCase

from battlefield.game.domain.entities import Player
from battlefield.game.domain.use_cases.game_status_getter import (
    GameStatusGetter,
    MoreThanExpected
)


class GameStatusGetterUnitTest(TestCase):
    def test_perform_returns_game_state_when_list_empty(self):
        game = GameStatusGetter().perform()

        assert game.player_one is None
        assert game.player_two is None

    def test_perform_returns_game_state_when_list_only_has_one_player(self):
        p1 = Player(1, 1)
        game = GameStatusGetter([p1]).perform()

        assert game.player_one is p1
        assert game.player_two is None

    def test_perform_raises_exception_when_two_players_join(
        self
    ):
        p1 = Player(1, 1)
        p2 = Player(2, 1)

        game = GameStatusGetter([p1, p2]).perform()
        assert game.player_one is p1
        assert game.player_two is p2

    def test_perform_raises_exception_when_an_additional_player_tries_to_join(
        self
    ):
        p1 = Player(1, 1)
        p2 = Player(2, 1)
        p3 = Player(3, 1)

        with self.assertRaises(MoreThanExpected):
            GameStatusGetter([p1, p2, p3]).perform()
