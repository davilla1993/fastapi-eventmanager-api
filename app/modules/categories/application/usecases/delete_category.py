from uuid import UUID

from app.modules.categories.domain.exceptions.category_exceptions import (
    CategoryNotFoundException,
)
from app.modules.categories.domain.repositories.category_repository import (
    AbstractCategoryRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class DeleteCategoryUseCase:
    def __init__(
        self, repository: AbstractCategoryRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(self, public_id: UUID, actor_public_id: UUID) -> None:
        category = await self._repository.find_by_public_id(public_id)
        if not category:
            raise CategoryNotFoundException(str(public_id))

        category.deleted_by = actor_public_id
        await self._repository.delete(category)
        await self._uow.commit()