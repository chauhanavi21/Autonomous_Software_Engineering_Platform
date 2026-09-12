import enum
from uuid import UUID
from sqlalchemy import Enum, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin

class ProjectStatus(str, enum.Enum): DRAFT="draft"; ACTIVE="active"; ARCHIVED="archived"
class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__="projects"
    __table_args__=(UniqueConstraint("workspace_id","slug",name="uq_project_workspace_slug"),)
    workspace_id: Mapped[UUID]=mapped_column(PGUUID(as_uuid=True),ForeignKey("workspaces.id",ondelete="CASCADE"),index=True)
    created_by: Mapped[UUID]=mapped_column(PGUUID(as_uuid=True),ForeignKey("users.id"),index=True)
    name: Mapped[str]=mapped_column(String(160),nullable=False)
    slug: Mapped[str]=mapped_column(String(180),nullable=False)
    description: Mapped[str | None]=mapped_column(Text,nullable=True)
    status: Mapped[ProjectStatus]=mapped_column(Enum(ProjectStatus,name="project_status"),default=ProjectStatus.DRAFT,nullable=False)
    repository_url: Mapped[str | None]=mapped_column(String(500),nullable=True)
    default_branch: Mapped[str]=mapped_column(String(120),default="main",nullable=False)
