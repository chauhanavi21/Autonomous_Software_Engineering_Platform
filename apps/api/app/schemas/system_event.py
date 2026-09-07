from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SystemEventCreate(BaseModel):
    event_type: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=2000)


class SystemEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_type: str
    message: str
    created_at: datetime
    updated_at: datetime
