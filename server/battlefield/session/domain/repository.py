from abc import ABCMeta, abstractmethod
from .entities import Session


class SessionRepository(ABCMeta):

    @abstractmethod
    def save(self, session: Session):
        pass
