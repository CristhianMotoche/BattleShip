from mapper.object_mapper import ObjectMapper
from battlefield.session.domain.entities import Session
from battlefield.session.data.db import SessionTable


class DataToDomain:
    def __init__(self, from_):
        self._from = from_

    @classmethod
    def map(cls):
        mapper = ObjectMapper()
        mapper.create_map(SessionTable, Session)
        return mapper.map(self._from)
