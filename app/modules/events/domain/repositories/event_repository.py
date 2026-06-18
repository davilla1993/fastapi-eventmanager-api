from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from app.modules.events.domain.entities.event import Event


class EventFilters:
    def __init__(
        self,
        city: str | None = None,
        event_type: str | None = None,
        category_public_id: UUID | None = None,
        organizer_public_id: UUID | None = None,
        date_min: datetime | None = None,
        date_max: datetime | None = None,
        price_max: Decimal | None = None,
        tags: list[str] | None = None,
        sort_by: str = "start_at",
        sort_order: str = "asc",
    ) -> None:
        self.city = city
        self.event_type = event_type
        self.category_public_id = category_public_id
        self.organizer_public_id = organizer_public_id
        self.date_min = date_min
        self.date_max = date_max
        self.price_max = price_max
        self.tags = tags
        self.sort_by = sort_by
        self.sort_order = sort_order


class AbstractEventRepository(ABC):
    @abstractmethod
    async def find_by_public_id(self, public_id: UUID) -> Event | None: ...

    @abstractmethod
    async def find_by_slug(self, slug: str) -> Event | None: ...

    @abstractmethod
    async def find_all(
        self, offset: int, limit: int, filters: EventFilters
    ) -> tuple[list[Event], int]: ...

    @abstractmethod
    async def save(self, event: Event) -> Event: ...

    @abstractmethod
    async def delete(self, event: Event) -> None: ...