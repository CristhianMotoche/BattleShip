from tests import client, app

from quart import url_for

import pytest


class TestAPI:

    pytestmark = pytest.mark.asyncio

    async def test_create(self, event_loop):
        async with app.app_context(), app.test_request_context('/ws'):
            url = url_for('session.create')
            resp = await client().post(url)
            assert resp.status_code == 200
