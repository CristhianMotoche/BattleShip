from unittest import TestCase, skip
from unittest.mock import create_autospec

from battlefield.game.domain.use_cases.play import Play
from battlefield.game.domain.entities import Game, Player, PlayerAction, PlayerPhase
from battlefield.game.domain.use_cases.responder import ResponderClient


class PlayUnitTest(TestCase):
    def test_perform_respons_to_player_with_message_when_not_enough_players(
        self,
    ) -> None:
        mock_responder = create_autospec(ResponderClient, spec_set=True)
        player = Player(1, 1, None)

        Play(Game(1), player, PlayerAction.PLACING, mock_responder).perform()

        mock_responder.send_to.assert_called_once_with(player, "Missing players")

    def test_perform_respons_to_player_with_message_when_too_many_players(
        self,
    ) -> None:
        mock_responder = create_autospec(ResponderClient, spec_set=True)
        player = Player(1, 1, None)
        game = Game(1)
        game.append(player)
        game.append(player)
        game.append(player)

        Play(game, player, PlayerAction.PLACING, mock_responder).perform()

        mock_responder.send_to.assert_called_once_with(player, "Too many players")

    @skip("NOT IMPLEMENTED YET")
    def test_perform_after_successfull_attack_changes_turn(
        self,
    ) -> None:
        mock_responder = create_autospec(ResponderClient, spec_set=True)
        player1 = Player(1, 1, None, PlayerPhase.READY)
        player2 = Player(2, 1, None, PlayerPhase.READY)
        game = Game(1)
        game.append(player1)
        game.append(player2)

        Play(game, player1, PlayerAction.ATTACKING, mock_responder).perform()

        assert game._turn == 1

    def test_perform_after_successfull_attack_from_second_player_changes_turn(
        self,
    ) -> None:
        mock_responder = create_autospec(ResponderClient, spec_set=True)
        player1 = Player(1, 1, None, PlayerPhase.READY)
        player2 = Player(2, 1, None, PlayerPhase.READY)
        game = Game(1)
        game.append(player1)
        game.append(player2)

        Play(game, player1, PlayerAction.ATTACKING, mock_responder).perform()
        Play(game, player2, PlayerAction.ATTACKING, mock_responder).perform()

        assert game._turn == 0

    @skip("NOT IMPLEMENTED YET")
    def test_perform_when_trying_to_attack_in_another_turn_sends_error_to_player(
        self,
    ) -> None:
        mock_responder = create_autospec(ResponderClient, spec_set=True)
        player1 = Player(1, 1, None, PlayerPhase.READY)
        player2 = Player(2, 1, None, PlayerPhase.READY)
        game = Game(1)
        game.append(player1)
        game.append(player2)

        Play(game, player2, PlayerAction.ATTACKING, mock_responder).perform()

        mock_responder.send_to.assert_called_once_with(player2, "Not your turn")
