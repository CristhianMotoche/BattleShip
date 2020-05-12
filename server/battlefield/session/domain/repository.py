from abc import ABC, abstractmethod
from .entities import Session
from typing import List


class SessionRepository(ABC):

    @abstractmethod
    def save(self, session: Session) -> Session:
        pass

    @abstractmethod
    def list(self) -> List[Session]:
        pass
