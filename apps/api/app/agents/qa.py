from pydantic import BaseModel, Field

from app.agents.base import AgentContext, BaseAgent


class QAOutput(BaseModel):
    summary: str
    unit_tests: list[str] = Field(default_factory=list)
    integration_tests: list[str] = Field(default_factory=list)
    edge_cases: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)


class QAAgent(BaseAgent):
    role = "qa"
    system_prompt = (
        "You are ForgeOS QAAgent. Find correctness, reliability, security, and regression "
        "risks. Return only valid JSON matching the requested schema."
    )
    output_model = QAOutput

    def build_prompt(self, context: AgentContext) -> str:
        return f"Create a rigorous test strategy for: {context.input_payload}"
