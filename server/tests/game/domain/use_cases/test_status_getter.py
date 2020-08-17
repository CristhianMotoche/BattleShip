from unittest import TestCase
from unittest.mock import Mock, create_autospec

from battlefield.game.domain.entities import Player
from battlefield.game.domain.use_cases.game_status_getter import (
    StatusGetter,
    GetterRepository,
    MoreThanExpected,
    NotEnoughPlayers,
    PlayerNotFound,
    WaitingPlayer,
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
        self.mock_repo.lookup_for_layers.return_
        with self.assertRaises(WaitingPlayer):
            StatusGetter(1, 1, [p1]).perform()

    def test_perform_raises_exception_when_two_players_join(self) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)

        game = StatusGetter(1, 1, [p1, p2]).perform()

        assert game.current_player is p1
        assert game.opponent_player is p2

    def test_perform_raises_exception_when_current_player_not_found(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)

        with self.assertRaises(PlayerNotFound):
            StatusGetter(123, 1, [p1, p2]).perform()

    def test_perform_raises_exception_when_more_than_expected(
        self,
    ) -> None:
        p1 = Player(1, 1, None)
        p2 = Player(2, 1, None)
        p3 = Player(3, 1, None)

        with self.assertRaises(MoreThanExpected):
            StatusGetter(1, 1, [p1, p2, p3]).perform()
