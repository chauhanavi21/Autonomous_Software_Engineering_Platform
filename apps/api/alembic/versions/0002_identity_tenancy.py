"""phase 2 identity and tenancy
Revision ID: 0002
Revises: 0001
"""
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql
revision="0002"; down_revision="0001"; branch_labels=None; depends_on=None

def timestamps():
    return [sa.Column("id",postgresql.UUID(as_uuid=True),primary_key=True),sa.Column("created_at",sa.DateTime(timezone=True),server_default=sa.text("now()"),nullable=False),sa.Column("updated_at",sa.DateTime(timezone=True),server_default=sa.text("now()"),nullable=False)]
def upgrade():
    role=sa.Enum("OWNER","ADMIN","DEVELOPER","VIEWER",name="organization_role"); status=sa.Enum("DRAFT","ACTIVE","ARCHIVED",name="project_status")
    op.create_table("users",sa.Column("email",sa.String(320),nullable=False),sa.Column("password_hash",sa.String(255),nullable=False),sa.Column("display_name",sa.String(120),nullable=False),sa.Column("is_active",sa.Boolean(),nullable=False,server_default=sa.true()),sa.Column("is_verified",sa.Boolean(),nullable=False,server_default=sa.false()),*timestamps(),sa.UniqueConstraint("email")); op.create_index("ix_users_email","users",["email"],unique=True)
    op.create_table("organizations",sa.Column("name",sa.String(120),nullable=False),sa.Column("slug",sa.String(140),nullable=False),sa.Column("created_by",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),*timestamps(),sa.UniqueConstraint("slug")); op.create_index("ix_organizations_slug","organizations",["slug"],unique=True)
    op.create_table("organization_memberships",sa.Column("organization_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("organizations.id",ondelete="CASCADE"),nullable=False),sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),sa.Column("role",role,nullable=False),*timestamps(),sa.UniqueConstraint("organization_id","user_id",name="uq_membership_org_user"))
    op.create_table("workspaces",sa.Column("organization_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("organizations.id",ondelete="CASCADE"),nullable=False),sa.Column("name",sa.String(120),nullable=False),sa.Column("slug",sa.String(140),nullable=False),*timestamps(),sa.UniqueConstraint("organization_id","slug",name="uq_workspace_org_slug"))
    op.create_table("projects",sa.Column("workspace_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("workspaces.id",ondelete="CASCADE"),nullable=False),sa.Column("created_by",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id"),nullable=False),sa.Column("name",sa.String(160),nullable=False),sa.Column("slug",sa.String(180),nullable=False),sa.Column("description",sa.Text()),sa.Column("status",status,nullable=False,server_default="DRAFT"),sa.Column("repository_url",sa.String(500)),sa.Column("default_branch",sa.String(120),nullable=False,server_default="main"),*timestamps(),sa.UniqueConstraint("workspace_id","slug",name="uq_project_workspace_slug"))
    op.create_table("refresh_tokens",sa.Column("user_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id",ondelete="CASCADE"),nullable=False),sa.Column("token_hash",sa.String(64),nullable=False),sa.Column("jti",sa.String(64),nullable=False),sa.Column("expires_at",sa.DateTime(timezone=True),nullable=False),sa.Column("revoked_at",sa.DateTime(timezone=True)),*timestamps(),sa.UniqueConstraint("token_hash"),sa.UniqueConstraint("jti"))
    op.create_table("audit_events",sa.Column("actor_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("users.id",ondelete="SET NULL")),sa.Column("organization_id",postgresql.UUID(as_uuid=True),sa.ForeignKey("organizations.id",ondelete="CASCADE")),sa.Column("event_type",sa.String(120),nullable=False),sa.Column("resource_type",sa.String(80)),sa.Column("resource_id",sa.String(80)),sa.Column("request_id",sa.String(80)),sa.Column("metadata_json",postgresql.JSONB(),nullable=False,server_default=sa.text("'{}'::jsonb")),*timestamps())
def downgrade():
    for table in ["audit_events","refresh_tokens","projects","workspaces","organization_memberships","organizations","users"]: op.drop_table(table)
    sa.Enum(name="project_status").drop(op.get_bind(),checkfirst=True); sa.Enum(name="organization_role").drop(op.get_bind(),checkfirst=True)
