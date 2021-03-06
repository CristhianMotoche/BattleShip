from battlefield.session.domain.entities import Session


class DataToDomain:
    def __init__(self, from_):
        self._from = from_

    def map(self):
        return Session(
            id=self._from.id,
            key=self._from.key,
        )
