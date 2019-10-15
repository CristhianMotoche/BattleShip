from random import shuffle
from ..entities import Session
from ..repository import SessionRepository


class SessionCreator:
    MAX_SIZE = 8

    def __init__(self, saver: SessionRepository):
        self._saver = saver

    def create(self):
        key = self.__gen_key()
        session = Session(key=key)
        self._saver.save(session)
        return session

    def __gen_key(self):
        return shuffle(string.ascii_letters)[:self.MAX_SIZE]
