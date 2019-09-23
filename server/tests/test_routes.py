from tests import client, app

from quart import url_for

import pytest


class TestRoutes:

    pytestmark = pytest.mark.asyncio

    async def test_echo_ws(self, event_loop):
        async with app.app_context(), app.test_request_context('/ws'):
            async with client().websocket(url_for('ws')) as ws:
                await ws.send('LOL')
                data = await ws.receive()
                assert data == 'START: LOL'
