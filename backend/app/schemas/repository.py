from pydantic import BaseModel, ConfigDict
from datetime import datetime


class RepositoryBase(BaseModel):
    name: str
    url: str


class RepositoryCreate(RepositoryBase):
    pass


class RepositoryResponse(RepositoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime
