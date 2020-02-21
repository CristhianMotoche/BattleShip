from ..domain.repository import SessionRepository
from .db import SessionTable
from ..domain.entities import Session
from typing import List


class SessionDataAccess(SessionRepository):

    async def save(self, session: Session):
        await SessionTable(key=session.key).save()

    async def list(self) -> List[Session]:
        sessions_db = await SessionTable.all()
        return map(lambda s: Session(id=s.id, key=s.key), sessions_db)
