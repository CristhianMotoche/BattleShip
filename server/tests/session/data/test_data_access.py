import pytest

from battlefield.session.data.data_access import SessionDataAccess

from battlefield.session.domain.entities import Session


class TestSessionDataAccess:

    pytestmark = pytest.mark.asyncio

    async def test_list_returns_an_empty_list_when_no_data(self, app):
        resp = await SessionDataAccess().list()
        assert list(resp) == []

    async def test_list_returns_two_elemens_inserted(self, app):
        await SessionDataAccess().save(Session(id=1, key='1234'))
        await SessionDataAccess().save(Session(id=2, key='1235'))

        resp = await SessionDataAccess().list()

        assert len(list(resp)) == 2
