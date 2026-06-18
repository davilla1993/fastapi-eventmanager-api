import uuid
from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, Field


class _EventReadBase(BaseModel):
    public_id: uuid.UUID
    title: str
    slug: str
    status: str
    start_at: datetime
    end_at: datetime
    city: str
    price: Decimal | None
    capacity: int | None
    image_url: str | None
    tags: str | None
    venue_public_id: uuid.UUID
    organizer_public_id: uuid.UUID
    category_public_id: uuid.UUID | None

    model_config = {"from_attributes": True}


class ConcertRead(_EventReadBase):
    event_type: Literal["concert"] = "concert"
    artist: str | None
    genre: str | None


class TheatreRead(_EventReadBase):
    event_type: Literal["theatre"] = "theatre"
    director: str | None
    cast_members: str | None


class ConferenceRead(_EventReadBase):
    event_type: Literal["conference"] = "conference"
    speaker: str | None
    topic: str | None


EventRead = Annotated[
    ConcertRead | TheatreRead | ConferenceRead,
    Field(discriminator="event_type"),
]


class _EventReadDetailBase(_EventReadBase):
    description: str | None
    created_at: datetime
    updated_at: datetime


class ConcertReadDetail(_EventReadDetailBase):
    event_type: Literal["concert"] = "concert"
    artist: str | None
    genre: str | None


class TheatreReadDetail(_EventReadDetailBase):
    event_type: Literal["theatre"] = "theatre"
    director: str | None
    cast_members: str | None


class ConferenceReadDetail(_EventReadDetailBase):
    event_type: Literal["conference"] = "conference"
    speaker: str | None
    topic: str | None


EventReadDetail = Annotated[
    ConcertReadDetail | TheatreReadDetail | ConferenceReadDetail,
    Field(discriminator="event_type"),
]