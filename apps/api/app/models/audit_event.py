from uuid import UUID
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.base_mixins import TimestampMixin, UUIDPrimaryKeyMixin

class AuditEvent(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__="audit_events"
    actor_id: Mapped[UUID | None]=mapped_column(PGUUID(as_uuid=True),ForeignKey("users.id",ondelete="SET NULL"),nullable=True,index=True)
    organization_id: Mapped[UUID | None]=mapped_column(PGUUID(as_uuid=True),ForeignKey("organizations.id",ondelete="CASCADE"),nullable=True,index=True)
    event_type: Mapped[str]=mapped_column(String(120),index=True)
    resource_type: Mapped[str | None]=mapped_column(String(80),nullable=True)
    resource_id: Mapped[str | None]=mapped_column(String(80),nullable=True)
    request_id: Mapped[str | None]=mapped_column(String(80),nullable=True,index=True)
    metadata_json: Mapped[dict]=mapped_column(JSONB,default=dict,nullable=False)
