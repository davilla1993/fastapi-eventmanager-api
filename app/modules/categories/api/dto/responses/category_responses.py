import uuid
from datetime import datetime

from pydantic import BaseModel


class CategoryRead(BaseModel):
    public_id: uuid.UUID
    name: str
    slug: str
    color: str | None

    model_config = {"from_attributes": True}


class CategoryReadDetail(BaseModel):
    public_id: uuid.UUID
    name: str
    slug: str
    description: str | None
    color: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}