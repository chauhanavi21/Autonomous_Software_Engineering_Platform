from fastapi import APIRouter
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.system_events import router as system_events_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.organizations import router as organizations_router
from app.api.v1.endpoints.workspaces import router as workspaces_router
from app.api.v1.endpoints.projects import router as projects_router
api_router=APIRouter(); api_router.include_router(health_router); api_router.include_router(auth_router); api_router.include_router(organizations_router); api_router.include_router(workspaces_router); api_router.include_router(projects_router); api_router.include_router(system_events_router)
