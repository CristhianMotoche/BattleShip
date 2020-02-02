from quart import url_for

import pytest


class TestAPI:

    pytestmark = pytest.mark.asyncio

    async def test_create(self, app):
        async with app.test_request_context('/sessions'):
            url = url_for('SessionIndex')
            resp = await app.test_client().post(url)
            assert resp.status_code == 200

    async def test_list(self, app):
        async with app.test_request_context('/'):
            url = url_for('SessionIndex')
            resp = await app.test_client().get(url)
            assert resp.status_code == 200

    async def test_get_single(self, app):
        async with app.app_context(), app.test_request_context('/'):
            url = url_for('SessionSingle', session_id=1)
            resp = await app.test_client().get(url)
            assert resp.status_code == 200
