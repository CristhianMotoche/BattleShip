from ..domain.repository import SessionRepository
from ..domain.entities import Session
from .db import SessionTable
from typing import List


class SessionDataAccess(SessionRepository):

    async def save(self, session: Session) -> Session:
        record = SessionTable(key=session.key)
        await record.save()
        return Session(id=record.id, key=record.key)

    async def list(self) -> List[Session]:
        sessions_db = await SessionTable.all()
        return map(lambda s: Session(id=s.id, key=s.key), sessions_db)
