import asyncio
from typing import Any, Optional

from quart import Response, abort, current_app, websocket
from quart_openapi import PintBlueprint

from battlefield.game.domain.entities import PlayerAction, Player
from battlefield.game.domain.use_cases.responder import (
    Responder,
    ResponderClient,
)
from battlefield.game.domain.use_cases.updater import Updater
from battlefield.game.domain.use_cases.game_status_getter import (
    GameStatusGetter,
)

game = PintBlueprint("game", "game")


async def broadcast(session_id, message):
    for websock in current_app.clients:
        if session_id == websock[0]:
            await websock[1].send(f"{message}")


class WebsocketResponder(ResponderClient):
    async def send_to(self, player: Player, msg: str) -> None:
        if player.ws:
            await player.ws.send(msg)


def collect_websocket(func):
    async def wrapper(session_id, *args, **kwargs):
        if (
            len(
                list(
                    filter(
                        lambda ws: ws.session == session_id,
                        current_app.clients,
                    )
                )
            )
            > 1
        ):
            abort(403)
        current_app.clients.add(
            Player(session_id, websocket._get_current_object())
        )
        try:
            return await func(session_id, *args, **kwargs)
        finally:
            player = look_up_player(session_id, ws)
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


# async def battle(session_id, ws, data):
#     player = look_up_player(session_id, ws)
#     if player and player.turn == "Ours":
#         await send_to_others(session_id, data, ws)
#     else:
#         await ws.send("Is not your turn...")


def look_up_player(session_id: int, ws: Any) -> Optional[Player]:
    return next(
        (
            player
            for player in current_app.clients
            if player.session == session_id and player.websocket == ws
        ),
        None,
    )


def update_player_in_list(updated_player: Player) -> None:
    for idx, player in enumerate(current_app.clients):
        if player.id_ == updated_player.id_:
            current_app.clients[idx] = updated_player


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id) -> Response:
    while True:
        try:
            data = await websocket.receive()
            action = PlayerAction.from_str(data)

            player_id = id(websocket._get_current_object())
            current_game = GameStatusGetter(
                player_id, session_id, current_app.clients
            ).perform()
            updated_player = Updater(
                current_game.current_player,
                action,
                data,
                current_game.get_status(),
            ).perform()
            update_player_in_list(updated_player)
        except asyncio.CancelledError:
            raise
        else:
            Responder(
                action,
                updated_player.status,
                current_game,
                WebsocketResponder(),
            ).perform()
