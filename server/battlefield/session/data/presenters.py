class SessionPresenter:
    def __init__(self, session):
        self._session = session

    def to_dict(self):
        return {
            'id': self._session.id,
            'key': self._session.key,
        }
