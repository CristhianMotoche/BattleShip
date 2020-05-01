import asyncio

from quart import abort, websocket
from quart import current_app
from quart_openapi import PintBlueprint

game = PintBlueprint("game", "game")


async def broadcast(session_id, message):
    for websock in current_app.clients:
        if session_id == websock[0]:
            await websock[1].send(b"New connection")


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
            print("Gone forever...")
            raise
        await broadcast(session_id, f"echo {data}")
