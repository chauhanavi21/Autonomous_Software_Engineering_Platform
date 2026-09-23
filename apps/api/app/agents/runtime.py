import asyncio
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base import AgentContext
from app.agents.budget import ExecutionBudget
from app.agents.providers.factory import get_provider
from app.agents.registry import AgentRegistry
from app.models.agent import AgentDefinition
from app.models.agent_execution import AgentExecution, AgentExecutionStatus


class AgentRuntime:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def execute(
        self,
        definition: AgentDefinition,
        *,
        user_id: UUID,
        input_payload: dict,
    ) -> AgentExecution:
        execution = AgentExecution(
            agent_id=definition.id,
            project_id=definition.project_id,
            requested_by=user_id,
            status=AgentExecutionStatus.RUNNING,
            input_payload=input_payload,
            provider=definition.provider.value,
            model=definition.model,
            started_at=datetime.now(UTC),
        )
        self.session.add(execution)
        await self.session.flush()

        try:
            provider = get_provider(definition.provider.value)
            agent_type = AgentRegistry.resolve(definition.role)
            agent = agent_type(
                provider,
                definition.model,
                temperature=definition.temperature,
                budget=ExecutionBudget(
                    max_tokens=definition.max_tokens,
                    timeout_seconds=definition.timeout_seconds,
                    max_cost_usd=definition.max_cost_usd,
                ),
            )
            if definition.system_prompt:
                agent.system_prompt = definition.system_prompt

            result = await asyncio.wait_for(
                agent.execute(
                    AgentContext(
                        project_id=str(definition.project_id),
                        user_id=str(user_id),
                        input_payload=input_payload,
                    )
                ),
                timeout=definition.timeout_seconds,
            )
            execution.status = AgentExecutionStatus.SUCCEEDED
            execution.raw_output = result.content
            execution.output_payload = result.structured_output
            execution.input_tokens = result.input_tokens
            execution.output_tokens = result.output_tokens
            execution.completed_at = datetime.now(UTC)
        except Exception as exc:
            execution.status = AgentExecutionStatus.FAILED
            execution.error_message = str(exc)[:2000]
            execution.completed_at = datetime.now(UTC)

        await self.session.commit()
        await self.session.refresh(execution)
        return execution
