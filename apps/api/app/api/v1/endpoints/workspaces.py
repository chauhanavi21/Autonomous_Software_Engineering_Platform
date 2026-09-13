from uuid import UUID
from fastapi import APIRouter
from sqlalchemy import select
from app.api.auth_dependencies import CurrentUser
from app.api.dependencies import DbSession
from app.auth.permissions import Permission
from app.models.workspace import Workspace
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from app.services.tenancy import membership_for, require_permission
router=APIRouter(tags=["Workspaces"])
@router.post("/organizations/{org_id}/workspaces",response_model=WorkspaceResponse,status_code=201)
async def create(org_id:UUID,body:WorkspaceCreate,user:CurrentUser,session:DbSession):
    await require_permission(session,user.id,org_id,Permission.WORKSPACE_CREATE); w=Workspace(organization_id=org_id,name=body.name,slug=body.slug); session.add(w); await session.commit(); await session.refresh(w); return w
@router.get("/organizations/{org_id}/workspaces",response_model=list[WorkspaceResponse])
async def list_ws(org_id:UUID,user:CurrentUser,session:DbSession):
    await membership_for(session,user.id,org_id); rows=await session.scalars(select(Workspace).where(Workspace.organization_id==org_id)); return list(rows)
