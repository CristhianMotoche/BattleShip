from unittest import TestCase
from unittest.mock import create_autospec

from battlefield.game.domain.entities import Player
from battlefield.game.domain.use_cases.game_status_getter import (
    StatusGetter,
    GetterRepository,
    MoreThanExpected,
    NotEnoughPlayers,
)


class GameStatusGetterUnitTest(TestCase):
    def setUp(self):
        self.mock_repo = create_autospec(GetterRepository, spec_set=True)

    def test_perform_raises_exception_when_player_list_is_empty(self) -> None:
        with self.assertRaises(NotEnoughPlayers):
            StatusGetter(1234, self.mock_repo).perform()

    def test_perform_raises_exception_when_only_one_player_in_list(
        self,
    ) -> None:
        p1 = Player(1, 1, None)

        self.mock_repo.lookup_for_players.return_value = [p1]

        with self.assertRaises(NotEnoughPlayers):
            StatusGetter(1, self.mock_repo).perform()

    def test_perform_returns_game_status_with_players(self) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)
        self.mock_repo.lookup_for_players.return_value = [p1, p2]

        game = StatusGetter(1, self.mock_repo).perform()

        assert game.current_player is p1
        assert game.opponent_player is p2

    def test_perform_raises_exception_when_more_than_expected(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)
        p3 = Player(3, 1, None)
        self.mock_repo.lookup_for_players.return_value = [p1, p2, p3]

        with self.assertRaises(MoreThanExpected):
            StatusGetter(1, self.mock_repo).perform()
