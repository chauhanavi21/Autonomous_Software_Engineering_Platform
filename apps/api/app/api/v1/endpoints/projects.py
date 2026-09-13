from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.auth_dependencies import CurrentUser
from app.api.dependencies import DbSession
from app.auth.permissions import Permission
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.services.tenancy import require_permission, workspace_with_membership
router=APIRouter(tags=["Projects"])
@router.post("/workspaces/{workspace_id}/projects",response_model=ProjectResponse,status_code=201)
async def create(workspace_id:UUID,body:ProjectCreate,user:CurrentUser,session:DbSession):
    w=await workspace_with_membership(session,user.id,workspace_id); await require_permission(session,user.id,w.organization_id,Permission.PROJECT_CREATE); p=Project(workspace_id=w.id,created_by=user.id,**body.model_dump()); session.add(p); await session.commit(); await session.refresh(p); return p
@router.get("/workspaces/{workspace_id}/projects",response_model=list[ProjectResponse])
async def list_projects(workspace_id:UUID,user:CurrentUser,session:DbSession):
    w=await workspace_with_membership(session,user.id,workspace_id); await require_permission(session,user.id,w.organization_id,Permission.PROJECT_READ); rows=await session.scalars(select(Project).where(Project.workspace_id==workspace_id)); return list(rows)
@router.get("/projects/{project_id}",response_model=ProjectResponse)
async def get_project(project_id:UUID,user:CurrentUser,session:DbSession):
    p=await session.get(Project,project_id)
    if not p: raise HTTPException(404,"Resource not found")
    w=await workspace_with_membership(session,user.id,p.workspace_id); await require_permission(session,user.id,w.organization_id,Permission.PROJECT_READ); return p
@router.patch("/projects/{project_id}",response_model=ProjectResponse)
async def update_project(project_id:UUID,body:ProjectUpdate,user:CurrentUser,session:DbSession):
    p=await session.get(Project,project_id)
    if not p: raise HTTPException(404,"Resource not found")
    w=await workspace_with_membership(session,user.id,p.workspace_id); await require_permission(session,user.id,w.organization_id,Permission.PROJECT_UPDATE)
    for k,v in body.model_dump(exclude_unset=True).items(): setattr(p,k,v)
    await session.commit(); await session.refresh(p); return p
