from battlefield import create_app

import pytest


@pytest.fixture(name='app')
async def _app():
    app = create_app('test')
    await app.startup()
    yield app
    await app.shutdown()
