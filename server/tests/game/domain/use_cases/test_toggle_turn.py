from unittest import TestCase

from battlefield.game.domain.entities import Player, Turn
from battlefield.game.domain.use_cases.toggle_turn import toggle_turn


class PlayerUnitTest(TestCase):
    def test_toggle_turn_changes_current_status(self) -> None:
        p = Player(1, 1, turn=Turn.Ours)
        assert toggle_turn(p).turn == Turn.Theirs

    def test_toggle_turn_does_not_change_status_when_None(self) -> None:
        p = Player(1, 1, turn=None)
        assert toggle_turn(p).turn is None
