from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ToolResult:
    ok: bool
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class AgentTool(ABC):
    name: str
    description: str

    @abstractmethod
    async def execute(self, arguments: dict[str, Any]) -> ToolResult:
        raise NotImplementedError
