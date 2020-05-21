from unittest import TestCase
from unittest.mock import MagicMock

from battlefield.game.domain.entities import (
    Player,
    PlayerAction,
    GameState,
)
from battlefield.game.domain.use_cases.responder import (
    Responder,
    ResponderClient,
)


class ResponderMock(ResponderClient):
    def send_to(self, other, msg):
        pass


class ResponderUnitTest(TestCase):
    def setUp(self) -> None:
        self.p1 = Player(1, 1, None)
        self.p2 = Player(1, 1, None)
        self.game = GameState(self.p1, self.p2)

    def test_perform_calls_client_with_Placing_when_action_is_Placing(
        self,
    ) -> None:
        action = PlayerAction.PLACING
        client_mock = ResponderMock()
        client_mock.send_to = MagicMock(return_value=None)

        Responder(action, self.game, client_mock).perform()

        client_mock.send_to.assert_called_with(self.p2, "Placing")

    def test_perform_calls_client_with_Ready_when_action_is_Ready(
        self,
    ) -> None:
        action = PlayerAction.READY
        client_mock = ResponderMock()
        client_mock.send_to = MagicMock(return_value=None)

        Responder(action, self.game, client_mock).perform()

        client_mock.send_to.assert_called_with(self.p2, "Ready")

    def test_perform_calls_client_with_Playing_when_action_is_Playing(
        self,
    ) -> None:
        action = PlayerAction.PLAYING
        client_mock = ResponderMock()
        client_mock.send_to = MagicMock(return_value=None)

        Responder(action, self.game, client_mock).perform()

        client_mock.send_to.assert_called_with(self.p2, "Playing")

    def test_perform_calls_own_client_with_invalid_action_when_action_is_unknown(
        self,
    ) -> None:
        action = PlayerAction.UNKNOWN
        client_mock = ResponderMock()
        client_mock.send_to = MagicMock(return_value=None)

        Responder(action, self.game, client_mock).perform()

        client_mock.send_to.assert_called_with(self.p1, "Invalid action")
