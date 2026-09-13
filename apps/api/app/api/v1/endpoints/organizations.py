from uuid import UUID
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.api.auth_dependencies import CurrentUser
from app.api.dependencies import DbSession
from app.auth.permissions import Permission
from app.models.membership import OrganizationMembership, Role
from app.models.organization import Organization
from app.models.workspace import Workspace
from app.schemas.organization import OrganizationCreate, OrganizationResponse, MemberResponse, MemberRoleUpdate
from app.services.tenancy import membership_for, require_permission
router=APIRouter(prefix="/organizations",tags=["Organizations"])
@router.post("",response_model=OrganizationResponse,status_code=201)
async def create(body:OrganizationCreate,user:CurrentUser,session:DbSession):
    if await session.scalar(select(Organization).where(Organization.slug==body.slug)): raise HTTPException(409,"Organization slug already exists")
    org=Organization(name=body.name,slug=body.slug,created_by=user.id); session.add(org); await session.flush(); session.add(OrganizationMembership(organization_id=org.id,user_id=user.id,role=Role.OWNER)); session.add(Workspace(organization_id=org.id,name="Default",slug="default")); await session.commit(); await session.refresh(org); return org
@router.get("",response_model=list[OrganizationResponse])
async def list_orgs(user:CurrentUser,session:DbSession):
    result=await session.scalars(select(Organization).join(OrganizationMembership).where(OrganizationMembership.user_id==user.id)); return list(result)
@router.get("/{org_id}/members",response_model=list[MemberResponse])
async def members(org_id:UUID,user:CurrentUser,session:DbSession):
    await membership_for(session,user.id,org_id); rows=await session.scalars(select(OrganizationMembership).where(OrganizationMembership.organization_id==org_id)); return [MemberResponse(user_id=m.user_id,role=m.role) for m in rows]
@router.patch("/{org_id}/members/{member_id}",response_model=MemberResponse)
async def update_role(org_id:UUID,member_id:UUID,body:MemberRoleUpdate,user:CurrentUser,session:DbSession):
    await require_permission(session,user.id,org_id,Permission.MEMBER_MANAGE); m=await session.scalar(select(OrganizationMembership).where(OrganizationMembership.organization_id==org_id,OrganizationMembership.user_id==member_id));
    if not m: raise HTTPException(404,"Resource not found")
    if m.role==Role.OWNER: raise HTTPException(400,"Owner role cannot be changed here")
    if body.role==Role.OWNER: raise HTTPException(400,"Ownership transfer is not supported in Phase 2")
    m.role=body.role; await session.commit(); return MemberResponse(user_id=m.user_id,role=m.role)
