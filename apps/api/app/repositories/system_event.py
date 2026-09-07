from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system_event import SystemEvent
from app.repositories.base import BaseRepository


class SystemEventRepository(BaseRepository[SystemEvent]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, SystemEvent)

    async def list_recent(self, limit: int = 20) -> list[SystemEvent]:
        result = await self.session.execute(
            select(SystemEvent).order_by(SystemEvent.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())
