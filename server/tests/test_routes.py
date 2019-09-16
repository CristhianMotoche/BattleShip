from tests import client

import pytest


class TestRoutes:
    pytestmark = pytest.mark.asyncio

    async def test_echo(self, event_loop):
        async with client().websocket('/ws') as ws:
            await ws.send('Echo works!')
            data = await ws.receive()
            assert data == 'Echo works!'
