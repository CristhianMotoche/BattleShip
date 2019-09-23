from quart import Quart, websocket
from battlefield.utils import init


def create_app(config):
    app = Quart(__name__)
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

    return app
