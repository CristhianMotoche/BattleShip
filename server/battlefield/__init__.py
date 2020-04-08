from quart import websocket
from quart_openapi import Pint
from quart_cors import cors
from battlefield.utils import init
from battlefield.utils.json import Encoder
from dotenv import load_dotenv

from tortoise import Tortoise

import asyncio


import json


BASE_MODEL_SCHEMA = {
    "$schema": "http://json-schema.org/schema#",
    "$id": "schema.json",
    "components": {
        "schemas": {
            "Session": {
                "type": "object",
                "properties": {
                    "id": {"type": "int"},
                    "key": {"type": "string"},
                },
                "required": ["id", "key"],
            }
        },
    },
}


def create_app(config):
    load_dotenv(verbose=True)

    app = Pint(
        __name__, title="BattleShip", base_model_schema=BASE_MODEL_SCHEMA
    )
    app = cors(app, allow_origin="*")
    app.json_encoder = Encoder

    app.config.from_envvar("CONFIG_FILE")

    app.clients = set()

    def collect_websocket(func):
        async def wrapper(session_id, *args, **kwargs):
            if len(list(filter(lambda ws: ws[0] == session_id, app.clients))) > 1:
                await websocket.send(f"NO MORE PLAYERS ARE ALLOWED! GET OUT!")
            app.clients.add((session_id, websocket._get_current_object()))
            try:
                return await func(session_id, *args, **kwargs)
            finally:
                app.clients.remove((session_id, websocket._get_current_object()))
        return wrapper

    async def broadcast(session_id, message):
        for websock in app.clients:
            if session_id == websock[0]:
                await websock[1].send(b'New connection')

    @app.before_serving
    async def init_orm():
        await init()

    from battlefield.session.data.api.single import session
    app.register_blueprint(session)

    from battlefield.session.data.api.multi import sessions
    app.register_blueprint(sessions)

    @app.websocket('/ws/session/<int:session_id>')
    @collect_websocket
    async def ws(session_id):
        while True:
            try:
                data = await websocket.receive()
            except asyncio.CancelledError:
                print("Gone forever...")
                raise
            await broadcast(session_id, f"echo {data}")

    @app.cli.command()
    def openapi():
        print(json.dumps(app.__schema__, indent=4, sort_keys=False))

    @app.after_serving
    async def close_orm():
        await Tortoise.close_connections()

    return app
