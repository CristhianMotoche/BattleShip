from unittest import TestCase
from unittest.mock import create_autospec

from battlefield.game.domain.use_cases.play import Play
from battlefield.game.domain.entities import Game, Player, PlayerAction
from battlefield.game.domain.use_cases.responder import ResponderClient


class PlayUnitTest(TestCase):
    def test_perform_respons_to_player_with_message_when_not_enough_players(
        self,
    ) -> None:
        mock_responder = create_autospec(ResponderClient, spec_set=True)
        player = Player(1, 1, None)

        Play(Game(1), player, PlayerAction.PLACING, mock_responder).perform()

        mock_responder.send_to.assert_called_once_with(player, "Missing players")
