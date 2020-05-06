from typing import Any, NamedTuple

import asyncio

from quart import abort, websocket
from quart import current_app
from quart_openapi import PintBlueprint

game = PintBlueprint("game", "game")


class Player(NamedTuple):
    session: int
    websocket: Any
    status: str = "PlacingShips"

    def __eq__(self, other):
        return (
            self.session == other.session and self.websocket == other.websocket
        )


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
            current_app.clients.remove(
                Player(session_id, websocket._get_current_object())
            )

    return wrapper


def update_status(data: str, session_id: int, ws: Any) -> None:
    player = next(
        (
            player
            for player in current_app.clients
            if player.session == session_id and player.websocket == ws
        ),
        None,
    )
    if player:
        remove_player = next(
            (
                player
                for player in current_app.clients
                if player.session == session_id and player.websocket == ws
            ),
            None,
        )
        if remove_player:
            current_app.clients.remove(remove_player)
            current_app.clients.add(Player(session_id, ws, data))


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id):
    while True:
        try:
            data = await websocket.receive()
            update_status(data, session_id, websocket._get_current_object())
        except asyncio.CancelledError:
            raise
        else:
            await send_to_others(
                session_id, data, websocket._get_current_object()
            )
