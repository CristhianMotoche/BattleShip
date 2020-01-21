from quart import websocket
from quart_openapi import Pint, OpenApiView
from battlefield.utils import init
import json


def create_app(config):
    app = Pint(__name__, title='BattleShip')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/gino'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    @app.before_serving
    async def init_orm():
        await init()

    @app.websocket('/ws')
    async def ws():
        while True:
            data = await websocket.receive()
            await websocket.send("START: %s" % data)

    from battlefield.session import session as session_bp
    app.register_blueprint(session_bp)

    @app.cli.command()
    def openapi():
        print(json.dumps(app.__schema__, indent=4, sort_keys=False))

    return app
