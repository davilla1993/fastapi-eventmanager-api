from uuid import UUID

from app.modules.events.domain.exceptions.event_exceptions import EventNotFoundException
from app.modules.events.domain.repositories.event_repository import (
    AbstractEventRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class DeleteEventUseCase:
    def __init__(
        self, repository: AbstractEventRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(self, public_id: UUID, actor_public_id: UUID) -> None:
        event = await self._repository.find_by_public_id(public_id)
        if not event:
            raise EventNotFoundException(str(public_id))

        event.deleted_by = actor_public_id
        await self._repository.delete(event)
        await self._uow.commit()