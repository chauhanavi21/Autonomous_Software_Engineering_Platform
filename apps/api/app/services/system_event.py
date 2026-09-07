from sqlalchemy.ext.asyncio import AsyncSession

from app.models.system_event import SystemEvent
from app.repositories.system_event import SystemEventRepository
from app.schemas.system_event import SystemEventCreate


class SystemEventService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repository = SystemEventRepository(session)

    async def create(self, payload: SystemEventCreate) -> SystemEvent:
        event = SystemEvent(event_type=payload.event_type, message=payload.message)
        event = await self.repository.add(event)
        await self.session.commit()
        return event

    async def list_recent(self, limit: int = 20) -> list[SystemEvent]:
        return await self.repository.list_recent(limit=limit)
