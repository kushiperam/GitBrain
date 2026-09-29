from pydantic import BaseModel, ConfigDict
from datetime import datetime


class RepositoryBase(BaseModel):
    name: str
    url: str


class RepositoryCreate(RepositoryBase):
    source_type: str = "github"
    local_path: str | None = None


class RepositoryResponse(RepositoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
    source_type: str
    local_path: str | None = None