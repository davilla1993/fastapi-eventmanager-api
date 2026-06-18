from uuid import UUID

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repositories.event_repository import (
    AbstractEventRepository,
    EventFilters,
)

_SORTABLE = {"start_at", "price", "title"}


class SqlAlchemyEventRepository(AbstractEventRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_public_id(self, public_id: UUID) -> Event | None:
        result = await self._session.execute(
            select(Event).where(
                Event.public_id == public_id, Event.deleted.is_(False)
            )
        )
        return result.scalar_one_or_none()

    async def find_by_slug(self, slug: str) -> Event | None:
        result = await self._session.execute(
            select(Event).where(Event.slug == slug, Event.deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def find_all(
        self, offset: int, limit: int, filters: EventFilters
    ) -> tuple[list[Event], int]:
        base = select(Event).where(Event.deleted.is_(False))

        if filters.city:
            base = base.where(Event.city.ilike(f"%{filters.city}%"))
        if filters.event_type:
            base = base.where(Event.event_type == filters.event_type)
        if filters.category_public_id:
            base = base.where(Event.category_public_id == filters.category_public_id)
        if filters.organizer_public_id:
            base = base.where(
                Event.organizer_public_id == filters.organizer_public_id
            )
        if filters.date_min:
            base = base.where(Event.start_at >= filters.date_min)
        if filters.date_max:
            base = base.where(Event.start_at <= filters.date_max)
        if filters.price_max is not None:
            base = base.where(Event.price <= filters.price_max)
        if filters.tags:
            for tag in filters.tags:
                base = base.where(Event.tags.ilike(f"%{tag}%"))

        total_result = await self._session.execute(
            select(func.count()).select_from(base.subquery())
        )
        total: int = total_result.scalar_one()

        sort_col_name = filters.sort_by if filters.sort_by in _SORTABLE else "start_at"
        sort_col = getattr(Event, sort_col_name)
        sort_fn = asc if filters.sort_order == "asc" else desc

        items_result = await self._session.execute(
            base.order_by(sort_fn(sort_col)).offset(offset).limit(limit)
        )
        return list(items_result.scalars().all()), total

    async def save(self, event: Event) -> Event:
        self._session.add(event)
        await self._session.flush()
        await self._session.refresh(event)
        return event

    async def delete(self, event: Event) -> None:
        event.deleted = True
        self._session.add(event)
        await self._session.flush()