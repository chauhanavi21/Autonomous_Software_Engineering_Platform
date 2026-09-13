from pydantic import BaseModel, Field
from uuid import UUID
from app.models.project import ProjectStatus
class ProjectCreate(BaseModel): name:str=Field(min_length=2,max_length=160); slug:str=Field(pattern=r"^[a-z0-9-]+$"); description:str|None=None; repository_url:str|None=None
class ProjectUpdate(BaseModel): name:str|None=None; description:str|None=None; status:ProjectStatus|None=None; repository_url:str|None=None
class ProjectResponse(BaseModel):
    id:UUID; workspace_id:UUID; created_by:UUID; name:str; slug:str; description:str|None; status:ProjectStatus; repository_url:str|None; default_branch:str
    model_config={"from_attributes":True}
