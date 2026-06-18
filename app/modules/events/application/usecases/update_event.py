from uuid import UUID

from app.modules.events.api.dto.requests.event_requests import EventUpdate
from app.modules.events.api.dto.responses.event_responses import (
    ConcertReadDetail,
    ConferenceReadDetail,
    TheatreReadDetail,
)
from app.modules.events.application.mappers.event_mapper import EventMapper
from app.modules.events.domain.exceptions.event_exceptions import (
    EventNotFoundException,
    EventSlugAlreadyExistsException,
)
from app.modules.events.domain.repositories.event_repository import (
    AbstractEventRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork

_EventDetailUnion = ConcertReadDetail | TheatreReadDetail | ConferenceReadDetail

_UPDATABLE_FIELDS = [
    "title", "description", "status", "start_at", "end_at",
    "city", "price", "capacity", "tags",
    "artist", "genre", "director", "cast_members", "speaker", "topic",
]


class UpdateEventUseCase:
    def __init__(
        self, repository: AbstractEventRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(
        self, public_id: UUID, request: EventUpdate, actor_public_id: UUID
    ) -> _EventDetailUnion:
        event = await self._repository.find_by_public_id(public_id)
        if not event:
            raise EventNotFoundException(str(public_id))

        if request.slug is not None and str(request.slug) != event.slug:
            if await self._repository.find_by_slug(str(request.slug)):
                raise EventSlugAlreadyExistsException(str(request.slug))
            event.slug = str(request.slug)

        if request.image_url is not None:
            event.image_url = str(request.image_url)

        for field in _UPDATABLE_FIELDS:
            value = getattr(request, field, None)
            if value is not None:
                setattr(event, field, value)

        event.updated_by = actor_public_id
        saved = await self._repository.save(event)
        await self._uow.commit()
        return EventMapper.to_detail(saved)