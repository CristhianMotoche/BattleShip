from battlefield.session.domain.repository import SessionRepository
from battlefield.session.domain.entities import Session
from typing import List


class SessionTestRepo(SessionRepository):

    def __init__(self, test_list=[]):
        self.test_list = test_list

    def save(self, session: Session):
        pass

    def list(self) -> List[Session]:
        return self.test_list
