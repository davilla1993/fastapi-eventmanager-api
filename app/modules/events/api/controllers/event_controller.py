from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.security.dependencies import (
    CurrentUser,
    get_current_user,
    require_organizer,
)
from app.modules.events.api.dto.requests.event_requests import (
    ConcertCreate,
    ConferenceCreate,
    EventUpdate,
    TheatreCreate,
)
from app.modules.events.api.dto.responses.event_responses import (
    ConcertRead,
    ConcertReadDetail,
    ConferenceRead,
    ConferenceReadDetail,
    TheatreRead,
    TheatreReadDetail,
)
from app.modules.events.application.usecases.create_event import CreateEventUseCase
from app.modules.events.application.usecases.delete_event import DeleteEventUseCase
from app.modules.events.application.usecases.get_event import GetEventUseCase
from app.modules.events.application.usecases.list_events import ListEventsUseCase
from app.modules.events.application.usecases.update_event import UpdateEventUseCase
from app.modules.events.domain.repositories.event_repository import EventFilters
from app.modules.events.infrastructure.repositories.sqlalchemy_event_repository import (  # noqa: E501
    SqlAlchemyEventRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/events", tags=["Events"])

_EventCreateBody = Annotated[
    ConcertCreate | TheatreCreate | ConferenceCreate,
    Body(discriminator="event_type"),
]
_EventDetailUnion = ConcertReadDetail | TheatreReadDetail | ConferenceReadDetail
_EventReadUnion = ConcertRead | TheatreRead | ConferenceRead


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_event(
    body: _EventCreateBody,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(require_organizer),
) -> _EventDetailUnion:
    repo = SqlAlchemyEventRepository(db)
    uow = UnitOfWork(db)
    return await CreateEventUseCase(repo, uow).execute(body, current_user.public_id)


@router.get("")
async def list_events(
    pagination: PaginationParams = Depends(),
    city: str | None = Query(default=None),
    event_type: str | None = Query(default=None, description="concert | theatre | conference"),  # noqa: E501
    category_public_id: UUID | None = Query(default=None),
    organizer_public_id: UUID | None = Query(default=None),
    date_min: datetime | None = Query(default=None),
    date_max: datetime | None = Query(default=None),
    price_max: Decimal | None = Query(default=None),
    tags: str | None = Query(default=None, description="Tags séparés par des virgules"),
    sort_by: str = Query(default="start_at", description="start_at | price | title"),
    sort_order: str = Query(default="asc", description="asc | desc"),
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[_EventReadUnion]:
    repo = SqlAlchemyEventRepository(db)
    filters = EventFilters(
        city=city,
        event_type=event_type,
        category_public_id=category_public_id,
        organizer_public_id=organizer_public_id,
        date_min=date_min,
        date_max=date_max,
        price_max=price_max,
        tags=[t.strip() for t in tags.split(",")] if tags else None,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return await ListEventsUseCase(repo).execute(pagination, filters)


@router.get("/{public_id}")
async def get_event(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> _EventDetailUnion:
    repo = SqlAlchemyEventRepository(db)
    return await GetEventUseCase(repo).execute(public_id)


@router.patch("/{public_id}")
async def update_event(
    public_id: UUID,
    body: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(require_organizer),
) -> _EventDetailUnion:
    repo = SqlAlchemyEventRepository(db)
    uow = UnitOfWork(db)
    return await UpdateEventUseCase(repo, uow).execute(
        public_id, body, current_user.public_id
    )


@router.delete("/{public_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    public_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
) -> None:
    repo = SqlAlchemyEventRepository(db)
    uow = UnitOfWork(db)
    await DeleteEventUseCase(repo, uow).execute(public_id, current_user.public_id)