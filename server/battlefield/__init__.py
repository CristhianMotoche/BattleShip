from quart_openapi import Pint
from quart_cors import cors
from battlefield.utils import init
from battlefield.utils.json import Encoder
from dotenv import load_dotenv

from tortoise import Tortoise


import json


BASE_MODEL_SCHEMA = {
    "$schema": "http://json-schema.org/schema#",
    "$id": "schema.json",
    "components": {
        "schemas": {
            "Session": {
                "type": "object",
                "properties": {"id": {"type": "int"}, "key": {"type": "string"},},
                "required": ["id", "key"],
            }
        },
    },
}


def create_app(config):
    load_dotenv(verbose=True)

    app = Pint(__name__, title="BattleShip", base_model_schema=BASE_MODEL_SCHEMA)
    app = cors(app, allow_origin="*")
    app.json_encoder = Encoder

    app.config.from_envvar("CONFIG_FILE")

    @app.before_serving
    async def init_orm():
        await init()

    from battlefield.session.data.api import sessions, session

    app.register_blueprint(sessions)
    app.register_blueprint(session)

    @app.cli.command()
    def openapi():
        print(json.dumps(app.__schema__, indent=4, sort_keys=False))

    @app.after_serving
    async def close_orm():
        await Tortoise.close_connections()

    return app
