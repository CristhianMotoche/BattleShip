import asyncio
import logging
import sys
from typing import Awaitable, Any, Callable

from quart import Response, abort, current_app, websocket
from quart_openapi import PintBlueprint

from battlefield.game.domain.entities import PlayerAction, Player, Game
from battlefield.game.domain.use_cases.play import Play
from battlefield.game.domain.use_cases.responder import ResponderClient


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

        if len(cur_game) >= 2:
            abort(403)

        cur_game.append(player)

        try:
            return await func(session_id, *args, **kwargs)
        finally:
            cur_game.remove(player)

    return wrapper


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id: int) -> Response:
    while True:
        try:
            data = await websocket.receive()
            cur_game: Game = current_app.games[session_id]
            player_id = id(websocket._get_current_object())
            player = cur_game.get(player_id)
            action = PlayerAction.from_str(data)
            logger.info(
                f"Player {player_id} in session {session_id} action {data}"
            )

            if not player:
                abort(403)

            response = Play(
                cur_game,
                player,
                action,
                WebsocketResponder(),
            ).perform()

        except asyncio.CancelledError:
            logger.info(
                f"Player {player_id} disconnected from session {session_id}"
            )
            raise
        else:
            await response
