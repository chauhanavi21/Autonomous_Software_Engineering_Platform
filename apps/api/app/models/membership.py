import enum
from uuid import UUID
from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin

class Role(str, enum.Enum):
    OWNER="owner"; ADMIN="admin"; DEVELOPER="developer"; VIEWER="viewer"

class OrganizationMembership(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__="organization_memberships"
    __table_args__=(UniqueConstraint("organization_id","user_id",name="uq_membership_org_user"),)
    organization_id: Mapped[UUID]=mapped_column(PGUUID(as_uuid=True),ForeignKey("organizations.id",ondelete="CASCADE"),index=True)
    user_id: Mapped[UUID]=mapped_column(PGUUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),index=True)
    role: Mapped[Role]=mapped_column(Enum(Role,name="organization_role"),nullable=False)
