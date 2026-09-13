from uuid import UUID
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.permissions import Permission, has_permission
from app.models.membership import OrganizationMembership
from app.models.workspace import Workspace

async def membership_for(session:AsyncSession,user_id:UUID,org_id:UUID)->OrganizationMembership:
    m=await session.scalar(select(OrganizationMembership).where(OrganizationMembership.organization_id==org_id,OrganizationMembership.user_id==user_id))
    if not m: raise HTTPException(404,"Resource not found")
    return m
async def require_permission(session:AsyncSession,user_id:UUID,org_id:UUID,permission:Permission):
    m=await membership_for(session,user_id,org_id)
    if not has_permission(m.role,permission): raise HTTPException(403,"Permission denied")
    return m
async def workspace_with_membership(session:AsyncSession,user_id:UUID,workspace_id:UUID)->Workspace:
    w=await session.get(Workspace,workspace_id)
    if not w: raise HTTPException(404,"Resource not found")
    await membership_for(session,user_id,w.organization_id); return w
