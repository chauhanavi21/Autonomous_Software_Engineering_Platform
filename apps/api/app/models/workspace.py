from uuid import UUID
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin

class Workspace(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__="workspaces"
    __table_args__=(UniqueConstraint("organization_id","slug",name="uq_workspace_org_slug"),)
    organization_id: Mapped[UUID]=mapped_column(PGUUID(as_uuid=True),ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
    name: Mapped[str]=mapped_column(String(120),nullable=False)
    slug: Mapped[str]=mapped_column(String(140),nullable=False)
