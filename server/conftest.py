from battlefield import create_app
from tortoise import Tortoise

import pytest


@pytest.fixture(name='app')
async def _app():
    app = create_app('test')
    await app.startup()
    yield app
    await Tortoise._drop_databases()
    await app.shutdown()
