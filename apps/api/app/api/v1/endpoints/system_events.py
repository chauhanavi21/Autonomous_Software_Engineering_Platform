from fastapi import APIRouter, Query, status

from app.api.dependencies import DbSession
from app.schemas.system_event import SystemEventCreate, SystemEventRead
from app.services.system_event import SystemEventService

router = APIRouter(prefix="/system-events", tags=["System Events"])


@router.post("", response_model=SystemEventRead, status_code=status.HTTP_201_CREATED)
async def create_system_event(payload: SystemEventCreate, session: DbSession) -> SystemEventRead:
    event = await SystemEventService(session).create(payload)
    return SystemEventRead.model_validate(event)


@router.get("", response_model=list[SystemEventRead])
async def list_system_events(
    session: DbSession,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[SystemEventRead]:
    events = await SystemEventService(session).list_recent(limit=limit)
    return [SystemEventRead.model_validate(event) for event in events]
