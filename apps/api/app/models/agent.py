import enum
from uuid import UUID

from sqlalchemy import Boolean, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin


class AgentProvider(str, enum.Enum):
    MOCK = "mock"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"


class AgentDefinition(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "agent_definitions"

    project_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    role: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    system_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider: Mapped[AgentProvider] = mapped_column(
        Enum(AgentProvider, name="agent_provider"), default=AgentProvider.MOCK, nullable=False
    )
    model: Mapped[str] = mapped_column(String(160), default="forgeos-mock-v1", nullable=False)
    temperature: Mapped[float] = mapped_column(Float, default=0.2, nullable=False)
    max_tokens: Mapped[int] = mapped_column(Integer, default=4000, nullable=False)
    timeout_seconds: Mapped[int] = mapped_column(Integer, default=60, nullable=False)
    max_cost_usd: Mapped[float] = mapped_column(Float, default=0.50, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
