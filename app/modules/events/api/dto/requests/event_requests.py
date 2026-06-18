from datetime import datetime
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator

from app.shared.types.slug import Slug
from app.shared.types.url_image import URLImage


class _EventBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    slug: Slug
    description: str | None = Field(default=None, max_length=5000)
    status: Literal["draft", "published", "cancelled", "sold_out"] = "draft"
    start_at: datetime
    end_at: datetime
    venue_public_id: UUID
    organizer_public_id: UUID
    category_public_id: UUID | None = None
    city: str = Field(min_length=1, max_length=100)
    price: Decimal | None = Field(default=None, ge=0)
    capacity: int | None = Field(default=None, ge=1)
    image_url: URLImage | None = None
    tags: str | None = Field(  # noqa: E501
        default=None, max_length=500, description="Tags séparés par des virgules"
    )

    @model_validator(mode="after")
    def check_dates(self) -> "_EventBase":
        if self.end_at <= self.start_at:
            raise ValueError("La date de fin doit être postérieure à la date de début.")
        return self


class ConcertCreate(_EventBase):
    event_type: Literal["concert"] = "concert"
    artist: str = Field(min_length=1, max_length=255)
    genre: str | None = Field(default=None, max_length=100)


class TheatreCreate(_EventBase):
    event_type: Literal["theatre"] = "theatre"
    director: str | None = Field(default=None, max_length=255)
    cast_members: str | None = Field(default=None, max_length=2000)


class ConferenceCreate(_EventBase):
    event_type: Literal["conference"] = "conference"
    speaker: str = Field(min_length=1, max_length=255)
    topic: str | None = Field(default=None, max_length=255)


EventCreate = Annotated[
    ConcertCreate | TheatreCreate | ConferenceCreate,
    Field(discriminator="event_type"),
]


class EventUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=255)
    slug: Slug | None = None
    description: str | None = Field(default=None, max_length=5000)
    status: Literal["draft", "published", "cancelled", "sold_out"] | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    city: str | None = Field(default=None, min_length=1, max_length=100)
    price: Decimal | None = Field(default=None, ge=0)
    capacity: int | None = Field(default=None, ge=1)
    image_url: URLImage | None = None
    tags: str | None = Field(default=None, max_length=500)
    artist: str | None = Field(default=None, max_length=255)
    genre: str | None = Field(default=None, max_length=100)
    director: str | None = Field(default=None, max_length=255)
    cast_members: str | None = Field(default=None, max_length=2000)
    speaker: str | None = Field(default=None, max_length=255)
    topic: str | None = Field(default=None, max_length=255)

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def allow_none(cls, v: object) -> object:
        return v