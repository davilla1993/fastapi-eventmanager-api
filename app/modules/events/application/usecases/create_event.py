from uuid import UUID

from app.modules.events.api.dto.requests.event_requests import (
    ConcertCreate,
    ConferenceCreate,
    TheatreCreate,
)
from app.modules.events.api.dto.responses.event_responses import (
    ConcertReadDetail,
    ConferenceReadDetail,
    TheatreReadDetail,
)
from app.modules.events.application.mappers.event_mapper import EventMapper
from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.exceptions.event_exceptions import (
    EventSlugAlreadyExistsException,
)
from app.modules.events.domain.repositories.event_repository import (
    AbstractEventRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork

_EventCreateUnion = ConcertCreate | TheatreCreate | ConferenceCreate
_EventDetailUnion = ConcertReadDetail | TheatreReadDetail | ConferenceReadDetail


class CreateEventUseCase:
    def __init__(
        self, repository: AbstractEventRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(
        self, request: _EventCreateUnion, actor_public_id: UUID
    ) -> _EventDetailUnion:
        if await self._repository.find_by_slug(str(request.slug)):
            raise EventSlugAlreadyExistsException(str(request.slug))

        data = request.model_dump()
        data["slug"] = str(request.slug)
        data["image_url"] = str(request.image_url) if request.image_url else None
        data["created_by"] = actor_public_id
        data["updated_by"] = actor_public_id

        event = Event(**data)
        saved = await self._repository.save(event)
        await self._uow.commit()
        return EventMapper.to_detail(saved)