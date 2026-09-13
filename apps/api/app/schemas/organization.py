from pydantic import BaseModel, Field
from uuid import UUID
from app.models.membership import Role
class OrganizationCreate(BaseModel): name:str=Field(min_length=2,max_length=120); slug:str=Field(pattern=r"^[a-z0-9-]+$",min_length=2,max_length=140)
class OrganizationResponse(BaseModel):
    id:UUID; name:str; slug:str
    model_config={"from_attributes":True}
class MemberResponse(BaseModel): user_id:UUID; role:Role
class MemberRoleUpdate(BaseModel): role:Role
