from app.agents.architect import ArchitectAgent
from app.agents.backend import BackendEngineerAgent
from app.agents.base import BaseAgent
from app.agents.qa import QAAgent


class AgentRegistry:
    _agents: dict[str, type[BaseAgent]] = {
        "architect": ArchitectAgent,
        "backend": BackendEngineerAgent,
        "qa": QAAgent,
    }

    @classmethod
    def resolve(cls, role: str) -> type[BaseAgent]:
        try:
            return cls._agents[role]
        except KeyError as exc:
            raise ValueError(f"Unknown agent role: {role}") from exc

    @classmethod
    def available_roles(cls) -> list[str]:
        return sorted(cls._agents)
