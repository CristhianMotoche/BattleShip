from quart import Quart, websocket


def create_app(config):
    app = Quart(__name__)

    @app.route('/')
    async def hello():
        return 'hello'

    @app.websocket('/ws')
    async def ws():
        while True:
            data = await websocket.receive()
            await websocket.send(f"{data}")

    return app
