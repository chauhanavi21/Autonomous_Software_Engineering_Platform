"""add agent runtime tables

Revision ID: 0003
Revises: 0002
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0003"
down_revision: str | None = "0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    agent_provider = sa.Enum("MOCK", "OPENAI", "ANTHROPIC", "GEMINI", name="agent_provider")
    execution_status = sa.Enum("PENDING", "RUNNING", "SUCCEEDED", "FAILED", name="agent_execution_status")
    agent_provider.create(op.get_bind(), checkfirst=True)
    execution_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "agent_definitions",
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("role", sa.String(length=80), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=True),
        sa.Column("provider", agent_provider, nullable=False),
        sa.Column("model", sa.String(length=160), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("max_tokens", sa.Integer(), nullable=False),
        sa.Column("timeout_seconds", sa.Integer(), nullable=False),
        sa.Column("max_cost_usd", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_definitions_project_id", "agent_definitions", ["project_id"])
    op.create_index("ix_agent_definitions_role", "agent_definitions", ["role"])

    op.create_table(
        "agent_executions",
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("requested_by", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", execution_status, nullable=False),
        sa.Column("input_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("output_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("raw_output", sa.Text(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("input_tokens", sa.Integer(), nullable=False),
        sa.Column("output_tokens", sa.Integer(), nullable=False),
        sa.Column("estimated_cost_usd", sa.Float(), nullable=False),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=160), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agent_definitions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requested_by"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agent_executions_agent_id", "agent_executions", ["agent_id"])
    op.create_index("ix_agent_executions_project_id", "agent_executions", ["project_id"])
    op.create_index("ix_agent_executions_requested_by", "agent_executions", ["requested_by"])
    op.create_index("ix_agent_executions_status", "agent_executions", ["status"])


def downgrade() -> None:
    op.drop_table("agent_executions")
    op.drop_table("agent_definitions")
    sa.Enum(name="agent_execution_status").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="agent_provider").drop(op.get_bind(), checkfirst=True)
