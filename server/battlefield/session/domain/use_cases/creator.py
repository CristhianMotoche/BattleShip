from random import choice
from string import ascii_letters
from ..entities import Session
from ..repository import SessionRepository


class SessionCreator:
    MAX_SIZE = 8

    def __init__(self, saver: SessionRepository):
        self._saver = saver

    async def create(self):
        key = self.__gen_key()
        session = Session(id=None, key=key)
        new_session = await self._saver.save(session)
        return new_session

    def __gen_key(self):
        return ''.join(choice(ascii_letters) for i in range(self.MAX_SIZE))
