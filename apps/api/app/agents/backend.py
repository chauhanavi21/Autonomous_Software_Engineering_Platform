from pydantic import BaseModel, Field

from app.agents.base import AgentContext, BaseAgent


class BackendOutput(BaseModel):
    summary: str
    api_changes: list[str] = Field(default_factory=list)
    data_changes: list[str] = Field(default_factory=list)
    implementation_steps: list[str] = Field(default_factory=list)
    tests: list[str] = Field(default_factory=list)


class BackendEngineerAgent(BaseAgent):
    role = "backend"
    system_prompt = (
        "You are ForgeOS BackendEngineerAgent. Produce implementation plans for secure, "
        "testable backend systems. Return only valid JSON matching the requested schema."
    )
    output_model = BackendOutput

    def build_prompt(self, context: AgentContext) -> str:
        return f"Plan the backend implementation for: {context.input_payload}"
