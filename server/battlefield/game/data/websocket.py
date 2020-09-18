import asyncio
import logging
import sys
from dataclasses import dataclass
from typing import Any, List

from quart import Response, abort, current_app, websocket
from quart_openapi import PintBlueprint

from battlefield.game.domain.entities import PlayerAction, Player
from battlefield.game.domain.use_cases.responder import (
    Responder,
    ResponderClient,
)
from battlefield.game.domain.use_cases.updater import Updater
from battlefield.game.domain.use_cases.game_status_getter import (
    GetterRepository,
    StatusGetter,
)

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "[%(asctime)s][%(levelname)s] %(name)s: %(message)s"
)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(consoleHandler)


game = PintBlueprint("game", "game")


class WebsocketResponder(ResponderClient):
    def send_to(self, player: Player, msg: str) -> Any:
        if player.ws:
            return player.ws.send(msg)


class Game:
    def __init__(self, session_id: int) -> None:
        self.session_id = session_id
        self._players: List[Player] = []

    def append(self, player: Player) -> None:
        self._players.append(player)

    def remove(self, player: Player) -> None:
        self._players.remove(player)

    def __len__(self) -> int:
        return len(self._players)


def collect_websocket(func):
    async def wrapper(session_id, *args, **kwargs):
        if session_id not in current_app.games:
            current_app.games[session_id] = Game(session_id)

        cur_game = current_app.games[session_id]

        if len(cur_game) > 2:
            abort(403)

        ws = websocket._get_current_object()
        player = Player(id(ws), session_id, ws)
        cur_game.append(player)

        try:
            return await func(session_id, *args, **kwargs)
        finally:
            cur_game.remove(player)

    return wrapper


def update_player_in_list(
    players: List[Player], old_player: Player, updated_player: Player
) -> None:
    players.remove(old_player)
    players.append(updated_player)


@dataclass(frozen=True)
class SessionRepo(GetterRepository):
    players: List[Player]

    def lookup_for_players(self, session_id: int) -> List[Player]:
        return [p for p in self.players if p.session == session_id]


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id: int) -> Response:
    while True:
        try:
            players = current_app.games[session_id]
            player_id = id(websocket._get_current_object())
            logger.info(
                f"Player {player_id} connected to session {session_id}"
            )

            data = await websocket.receive()
            action = PlayerAction.from_str(data)
            current_game = StatusGetter(
                session_id, SessionRepo(players)
            ).perform()
            updated_player = Updater(
                current_game.current_player,
                action,
                data,
                current_game.get_status(),
            ).perform()
            update_player_in_list(
                players, current_game.current_player, updated_player
            )
            response = Responder(
                action, current_game, WebsocketResponder(),
            ).perform()
        except asyncio.CancelledError:
            logger.info(
                f"Player {player_id} disconnected from session {session_id}"
            )
            raise
        else:
            await response
