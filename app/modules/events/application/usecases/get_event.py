from uuid import UUID

from app.modules.events.api.dto.responses.event_responses import (
    ConcertReadDetail,
    ConferenceReadDetail,
    TheatreReadDetail,
)
from app.modules.events.application.mappers.event_mapper import EventMapper
from app.modules.events.domain.exceptions.event_exceptions import EventNotFoundException
from app.modules.events.domain.repositories.event_repository import (
    AbstractEventRepository,
)


class GetEventUseCase:
    def __init__(self, repository: AbstractEventRepository) -> None:
        self._repository = repository

    async def execute(
        self, public_id: UUID
    ) -> ConcertReadDetail | TheatreReadDetail | ConferenceReadDetail:
        event = await self._repository.find_by_public_id(public_id)
        if not event:
            raise EventNotFoundException(str(public_id))
        return EventMapper.to_detail(event)