from dataclasses import dataclass

from battlefield.game.domain.entities import Player, PlayerAction, GamePhase


@dataclass
class Updater:

    current_player: Player
    action: PlayerAction
    game_phase: GamePhase

    def perform(self) -> Player:
        if self.action.is_placing() and self.game_phase.is_placing():
            return self.current_player.set_placing()
        elif self.action.is_ready() and self.game_phase.is_placing():
            return self.current_player.set_ready()
        elif self.action.is_playing() and self.game_phase.is_ready():
            return self.current_player.set_playing()
        elif self.action.is_attacking() and self.game_phase.is_playing():
            return self.current_player.set_attacking()
        return self.current_player
