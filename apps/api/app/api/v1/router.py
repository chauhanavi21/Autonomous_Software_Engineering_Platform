from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.system_events import router as system_events_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(system_events_router)
