import asyncio
import logging
import sys
from dataclasses import dataclass
from typing import Awaitable, Any, Callable, List

from quart import Response, abort, current_app, websocket
from quart_openapi import PintBlueprint

from battlefield.game.domain.entities import PlayerAction, Player, Game
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


def collect_websocket(
    func: Callable[..., Awaitable[Any]]
) -> Callable[..., Awaitable[Any]]:
    async def wrapper(session_id: int, *args, **kwargs):
        ws = websocket._get_current_object()
        player = Player(id(ws), session_id, ws)
        cur_game = current_app.games[session_id] = current_app.games.get(
            session_id, Game(session_id)
        )

        if len(cur_game) > 2:
            abort(403)

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
        return self.players


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id: int) -> Response:
    while True:
        try:
            cur_game = current_app.games[session_id]
            player_id = id(websocket._get_current_object())
            logger.info(
                f"Player {player_id} connected to session {session_id}"
            )

            data = await websocket.receive()
            action = PlayerAction.from_str(data)
            current_game = StatusGetter(
                session_id, SessionRepo(cur_game._players)
            ).perform()
            updated_player = Updater(
                current_game.current_player,
                action,
                data,
                current_game.get_status(),
            ).perform()
            update_player_in_list(
                cur_game._players, current_game.current_player, updated_player
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
