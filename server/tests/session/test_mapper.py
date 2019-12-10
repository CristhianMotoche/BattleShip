from unittest import TestCase
from battlefield.session.mappers import DataToDomain
from battlefield.session.domain.entities import Session
from battlefield.session.data.db import SessionTable


class TestDataToDomain(TestCase):

    def test_map_converts_a_sessiontable_to_a_session(self):
        from_ = SessionTable(key='12345678')

        instance_session = DataToDomain(from_).map()

        assert isinstance(instance_session, Session)
        assert instance_session.id == None
        assert instance_session.key == '12345678'
