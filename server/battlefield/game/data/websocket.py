import asyncio
from typing import Any, Optional

from quart import abort, current_app, websocket
from quart_openapi import PintBlueprint

from battlefield.game.domain.entities import Player
from battlefield.game.domain.use_cases.responder import Responder
from battlefield.game.domain.use_cases.updater import Updater
from battlefield.game.domain.use_cases.game_status_getter import GameStatusGetter

game = PintBlueprint("game", "game")


async def broadcast(session_id, message):
    for websock in current_app.clients:
        if session_id == websock[0]:
            await websock[1].send(f"{message}")


async def send_to_others(session_id, message, ws_sender):
    for ws in current_app.clients:
        if session_id == ws[0] and ws[1] != ws_sender:
            await ws[1].send(message)


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


async def battle(session_id, ws, data):
    player = look_up_player(session_id, ws)
    if player and player.turn == "Ours":
        await send_to_others(session_id, data, ws)
    else:
        await ws.send("Is not your turn...")


def look_up_player(session_id: int, ws: Any) -> Optional[Player]:
    return next(
        (
            player
            for player in current_app.clients
            if player.session == session_id and player.websocket == ws
        ),
        None,
    )


def update_status(data: str, session_id: int, ws: Any) -> None:
    player = look_up_player(session_id, ws)
    if player:
        current_app.clients.remove(player)
        current_app.clients.add(Player(session_id, ws, data))


def update_turn(turn: str, session_id: int, ws: Any) -> None:
    player = look_up_player(session_id, ws)
    if player:
        current_app.clients.remove(player)
        current_app.clients.add(Player(session_id, ws, "Playing", turn))


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id):
    while True:
        try:
            data = await websocket.receive()
            current_game = GameStatusGetter(current_app.clients).perform()
            update_resp = Updater(data, current_game).perform()
        except asyncio.CancelledError:
            raise
        else:
            Responder(update_resp).perform()
