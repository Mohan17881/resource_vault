from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResourceBase(BaseModel):
    title: str
    url: str
    tags: Optional[str] = ""
    source: Optional[str] = ""

class ResourceCreate(ResourceBase):
    pass

class Resource(ResourceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True