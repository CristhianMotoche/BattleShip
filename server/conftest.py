from battlefield import create_app

import pytest


@pytest.fixture(name='app')
def _app():
    app = create_app('test')
    return app
