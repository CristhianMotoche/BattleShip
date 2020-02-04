from abc import ABC, abstractmethod
from .entities import Session


class SessionRepository(ABC):

    @abstractmethod
    def save(self, session: Session):
        pass

    @abstractmethod
    def list(self):
        pass
