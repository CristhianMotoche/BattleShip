import pytest

from battlefield.session.data.data_access import SessionDataAccess


class TestSessionDataAccess:

    pytestmark = pytest.mark.asyncio

    async def test_list_returns_an_empty_list_when_no_data(self, app):
        resp = await SessionDataAccess().list()
        assert resp == []
