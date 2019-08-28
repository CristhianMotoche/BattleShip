from quart import Quart, websocket

app = Quart(__name__)

@app.route('/')
async def hello():
    return 'hello'

@app.websocket('/ws')
async def ws():
    while True:
        data = await websocket.receive()
        print(data)
        await websocket.send(f"Python: {data}")

app.run()
