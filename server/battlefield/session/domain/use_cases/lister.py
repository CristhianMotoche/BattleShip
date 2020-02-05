from ..entities import Session
from ..repository import SessionRepository
from typing import List


class SessionLister:

    def __init__(self, lister: SessionRepository):
        self._lister = lister

    def list(self) -> List[Session]:
        return self._lister.list()
