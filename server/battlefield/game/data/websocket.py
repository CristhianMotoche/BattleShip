import asyncio

from quart import abort, websocket
from quart import current_app
from quart_openapi import PintBlueprint

game = PintBlueprint("game", "game")


async def broadcast(session_id, message):
    for websock in current_app.clients:
        if session_id == websock[0]:
            await websock[1].send(f"{message}")


async def send_to_others(session_id, message, ws_sender):
    for ws in current_app.clients:
        if session_id == ws[0] and ws[1] != ws_sender:
            await ws[1].send (message)


def collect_websocket(func):
    async def wrapper(session_id, *args, **kwargs):
        if (
            len(
                list(
                    filter(lambda ws: ws[0] == session_id, current_app.clients)
                )
            )
            > 1
        ):
            abort(403)
        current_app.clients.add((session_id, websocket._get_current_object()))
        try:
            return await func(session_id, *args, **kwargs)
        finally:
            current_app.clients.remove(
                (session_id, websocket._get_current_object())
            )

    return wrapper


@game.websocket("/ws/session/<int:session_id>")
@collect_websocket
async def ws(session_id):
    while True:
        try:
            data = await websocket.receive()
        except asyncio.CancelledError:
            raise
        await send_to_others(session_id, f"{data}", websocket._get_current_object())
