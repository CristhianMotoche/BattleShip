from ..domain.repository import SessionRepository
from .db import SessionTable


class SessionDataAccess(SessionRepository):

    async def save(self, session):
        await SessionTable(key=session.key).save()
