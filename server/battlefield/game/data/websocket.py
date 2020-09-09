import asyncio
import logging
import sys
from dataclasses import dataclass
from typing import Any, Optional, List

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


async def broadcast(session_id, message):
    for websock in current_app.clients:
        if session_id == websock[0]:
            await websock[1].send(f"{message}")


class WebsocketResponder(ResponderClient):
    def send_to(self, player: Player, msg: str) -> Any:
        if player.ws:
            return player.ws.send(msg)


def collect_websocket(func):
    async def wrapper(session_id, *args, **kwargs):
        total_players_in_session = len(
            [
                player
                for player in current_app.clients
                if player.session == session_id
            ]
        )
        if total_players_in_session > 2:
            abort(403)
        ws = websocket._get_current_object()
        current_app.clients.add(Player(id(ws), session_id, ws))
        try:
            return await func(session_id, *args, **kwargs)
        finally:
            player = look_up_player(id(ws))
            if player:
                current_app.clients.remove(player)

    return wrapper


async def set_turn(session_id: int) -> None:
    players = list(
        filter(
            lambda player: player.session == session_id
            and player.status == "Playing"
            and player.turn == "None",
            current_app.clients,
        )
    )
    if len(players) == 2:
        await players[0].websocket.send("Ours")
        await players[1].websocket.send("Theirs")


def look_up_player(id_: int) -> Optional[Player]:
    return next(
        (player for player in current_app.clients if player.id_ == id_), None,
    )


def update_player_in_list(old_player: Player, updated_player: Player) -> None:
    current_app.clients.remove(old_player)
    current_app.clients.add(updated_player)


@dataclass(frozen=True)
class SessionRepo(GetterRepository):
    players: List[Player]

    def lookup_for_players(self, session_id: int) -> List[Player]:
        return [p for p in self.players if p.session == session_id]


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id) -> Response:
    while True:
        player_id = id(websocket._get_current_object())
        logger.info(f"Player {player_id} connected to session {session_id}")
        try:
            data = await websocket.receive()
            action = PlayerAction.from_str(data)

            current_game = StatusGetter(
                session_id, SessionRepo(current_app.clients)
            ).perform()
            updated_player = Updater(
                current_game.current_player,
                action,
                data,
                current_game.get_status(),
            ).perform()
            update_player_in_list(current_game.current_player, updated_player)
        except asyncio.CancelledError:
            logger.info(
                f"Player {player_id} disconnected from session {session_id}"
            )
            raise
        else:
            response = Responder(
                action, current_game, WebsocketResponder(),
            ).perform()
            await response
