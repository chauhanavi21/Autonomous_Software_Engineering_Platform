from typing import Literal

from pydantic import BaseModel


class ComponentHealth(BaseModel):
    status: Literal["healthy", "unhealthy"]
    latency_ms: float | None = None


class LiveHealthResponse(BaseModel):
    status: Literal["alive"]
    service: str


class ReadyHealthResponse(BaseModel):
    status: Literal["healthy", "degraded"]
    service: str
    database: ComponentHealth
    redis: ComponentHealth
