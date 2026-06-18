from app.modules.events.api.dto.responses.event_responses import (
    ConcertRead,
    ConferenceRead,
    TheatreRead,
)
from app.modules.events.application.mappers.event_mapper import EventMapper
from app.modules.events.domain.repositories.event_repository import (
    AbstractEventRepository,
    EventFilters,
)
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams

_EventReadUnion = ConcertRead | TheatreRead | ConferenceRead


class ListEventsUseCase:
    def __init__(self, repository: AbstractEventRepository) -> None:
        self._repository = repository

    async def execute(
        self, pagination: PaginationParams, filters: EventFilters
    ) -> PaginatedResponse[_EventReadUnion]:
        events, total = await self._repository.find_all(
            offset=pagination.offset, limit=pagination.size, filters=filters
        )
        return PaginatedResponse.create(
            items=[EventMapper.to_read(e) for e in events],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )