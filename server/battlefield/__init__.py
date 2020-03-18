from quart_openapi import Pint
from battlefield.utils import init
from battlefield.utils.json import Encoder

from tortoise import Tortoise


import json


def create_app(config):
    app = Pint(__name__, title='BattleShip')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gino'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.json_encoder = Encoder

    @app.before_serving
    async def init_orm():
        await init()

    from battlefield.session.data.api import Session
    app.add_url_rule("/sessions", view_func=Session.as_view("SessionIndex"))
    app.add_url_rule("/sessions/<int:session_id>",
                     view_func=Session.as_view("SessionSingle"))

    @app.cli.command()
    def openapi():
        print(json.dumps(app.__schema__, indent=4, sort_keys=False))

    @app.after_serving
    async def close_orm():
        await Tortoise.close_connections()

    return app
