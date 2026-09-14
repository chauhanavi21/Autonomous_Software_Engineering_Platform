from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, ValidationError

from app.agents.budget import ExecutionBudget
from app.agents.providers.base import ModelProvider, ModelRequest, ModelResponse
from app.agents.retry import RetryPolicy
from app.agents.tools.base import AgentTool


@dataclass(slots=True)
class AgentContext:
    project_id: str
    user_id: str
    input_payload: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AgentResult:
    content: str
    structured_output: dict[str, Any] | None
    input_tokens: int
    output_tokens: int
    provider_metadata: dict[str, Any]


class BaseAgent:
    role = "general"
    system_prompt = "You are a reliable software engineering agent."
    output_model: type[BaseModel] | None = None

    def __init__(
        self,
        provider: ModelProvider,
        model: str,
        *,
        temperature: float = 0.2,
        budget: ExecutionBudget | None = None,
        retry_policy: RetryPolicy | None = None,
        tools: list[AgentTool] | None = None,
    ) -> None:
        self.provider = provider
        self.model = model
        self.temperature = temperature
        self.budget = budget or ExecutionBudget()
        self.retry_policy = retry_policy or RetryPolicy()
        self.tools = {tool.name: tool for tool in (tools or [])}

    def build_prompt(self, context: AgentContext) -> str:
        return str(context.input_payload)

    async def execute(self, context: AgentContext) -> AgentResult:
        response: ModelResponse = await self.provider.generate(
            ModelRequest(
                system_prompt=self.system_prompt,
                user_prompt=self.build_prompt(context),
                model=self.model,
                temperature=self.temperature,
                max_tokens=min(self.budget.max_tokens, 4000),
                response_schema=(
                    self.output_model.model_json_schema() if self.output_model else None
                ),
            )
        )
        self.budget.ensure_token_budget(response.input_tokens + response.output_tokens)

        structured: dict[str, Any] | None = None
        if self.output_model:
            try:
                parsed = self.output_model.model_validate_json(response.content)
                structured = parsed.model_dump(mode="json")
            except ValidationError:
                structured = None

        return AgentResult(
            content=response.content,
            structured_output=structured,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            provider_metadata=response.metadata,
        )
