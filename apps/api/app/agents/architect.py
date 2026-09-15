from pydantic import BaseModel, Field

from app.agents.base import BaseAgent, AgentContext


class ArchitectureOutput(BaseModel):
    summary: str
    components: list[str] = Field(default_factory=list)
    data_stores: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)


class ArchitectAgent(BaseAgent):
    role = "architect"
    system_prompt = (
        "You are ForgeOS ArchitectAgent. Design maintainable software systems. "
        "Return only valid JSON matching the requested schema. Include tradeoffs, risks, "
        "service boundaries, persistence choices, and concrete next steps."
    )
    output_model = ArchitectureOutput

    def build_prompt(self, context: AgentContext) -> str:
        return (
            "Design the system requested below.\n"
            f"Project: {context.project_id}\n"
            f"Requirements: {context.input_payload}"
        )
