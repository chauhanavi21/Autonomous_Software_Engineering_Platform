from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app.agents.registry import AgentRegistry
from app.agents.runtime import AgentRuntime
from app.api.auth_dependencies import CurrentUser
from app.api.dependencies import DbSession
from app.auth.permissions import Permission
from app.models.agent import AgentDefinition
from app.models.agent_execution import AgentExecution
from app.models.project import Project
from app.schemas.agent import (
    AgentCreate,
    AgentExecuteRequest,
    AgentExecutionResponse,
    AgentResponse,
)
from app.services.tenancy import require_permission, workspace_with_membership

router = APIRouter(tags=["Agents"])


async def project_with_access(
    session: DbSession, user_id: UUID, project_id: UUID, permission: Permission
) -> Project:
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Resource not found")
    workspace = await workspace_with_membership(session, user_id, project.workspace_id)
    await require_permission(session, user_id, workspace.organization_id, permission)
    return project


@router.get("/agent-roles")
async def available_roles(user: CurrentUser) -> dict[str, list[str]]:
    return {"roles": AgentRegistry.available_roles()}


@router.post(
    "/projects/{project_id}/agents", response_model=AgentResponse, status_code=201
)
async def create_agent(
    project_id: UUID, body: AgentCreate, user: CurrentUser, session: DbSession
) -> AgentDefinition:
    await project_with_access(session, user.id, project_id, Permission.PROJECT_UPDATE)
    definition = AgentDefinition(project_id=project_id, **body.model_dump())
    session.add(definition)
    await session.commit()
    await session.refresh(definition)
    return definition


@router.get("/projects/{project_id}/agents", response_model=list[AgentResponse])
async def list_agents(
    project_id: UUID, user: CurrentUser, session: DbSession
) -> list[AgentDefinition]:
    await project_with_access(session, user.id, project_id, Permission.PROJECT_READ)
    rows = await session.scalars(
        select(AgentDefinition).where(AgentDefinition.project_id == project_id)
    )
    return list(rows)


@router.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID, user: CurrentUser, session: DbSession
) -> AgentDefinition:
    definition = await session.get(AgentDefinition, agent_id)
    if not definition:
        raise HTTPException(404, "Resource not found")
    await project_with_access(
        session, user.id, definition.project_id, Permission.PROJECT_READ
    )
    return definition


@router.post(
    "/agents/{agent_id}/execute", response_model=AgentExecutionResponse, status_code=201
)
async def execute_agent(
    agent_id: UUID,
    body: AgentExecuteRequest,
    user: CurrentUser,
    session: DbSession,
) -> AgentExecution:
    definition = await session.get(AgentDefinition, agent_id)
    if not definition or not definition.is_active:
        raise HTTPException(404, "Resource not found")
    await project_with_access(
        session, user.id, definition.project_id, Permission.PROJECT_UPDATE
    )
    runtime = AgentRuntime(session)
    return await runtime.execute(definition, user_id=user.id, input_payload=body.input)


@router.get(
    "/projects/{project_id}/agent-executions",
    response_model=list[AgentExecutionResponse],
)
async def list_executions(
    project_id: UUID, user: CurrentUser, session: DbSession
) -> list[AgentExecution]:
    await project_with_access(session, user.id, project_id, Permission.PROJECT_READ)
    rows = await session.scalars(
        select(AgentExecution)
        .where(AgentExecution.project_id == project_id)
        .order_by(AgentExecution.created_at.desc())
    )
    return list(rows)
