from pydantic import BaseModel, Field
from uuid import UUID
class WorkspaceCreate(BaseModel): name:str=Field(min_length=2,max_length=120); slug:str=Field(pattern=r"^[a-z0-9-]+$")
class WorkspaceResponse(BaseModel):
    id:UUID; organization_id:UUID; name:str; slug:str
    model_config={"from_attributes":True}
