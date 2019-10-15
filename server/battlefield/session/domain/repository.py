from abc import ABCMeta, abstractmethod
from .entities import Session


class SessionRepository(ABC):

    @abstractmethod
    def save(self, session: Session):
        pass
