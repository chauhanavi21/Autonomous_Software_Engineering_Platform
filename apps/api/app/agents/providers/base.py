from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ModelRequest:
    system_prompt: str
    user_prompt: str
    model: str
    temperature: float = 0.2
    max_tokens: int = 1200
    response_schema: dict[str, Any] | None = None


@dataclass(slots=True)
class ModelResponse:
    content: str
    input_tokens: int = 0
    output_tokens: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


class ModelProvider(ABC):
    name: str

    @abstractmethod
    async def generate(self, request: ModelRequest) -> ModelResponse:
        raise NotImplementedError
