from uuid import UUID

from app.modules.categories.api.dto.requests.category_requests import CategoryCreate
from app.modules.categories.api.dto.responses.category_responses import (
    CategoryReadDetail,
)
from app.modules.categories.application.mappers.category_mapper import CategoryMapper
from app.modules.categories.domain.entities.category import Category
from app.modules.categories.domain.exceptions.category_exceptions import (
    CategorySlugAlreadyExistsException,
)
from app.modules.categories.domain.repositories.category_repository import (
    AbstractCategoryRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class CreateCategoryUseCase:
    def __init__(
        self, repository: AbstractCategoryRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(
        self, request: CategoryCreate, actor_public_id: UUID
    ) -> CategoryReadDetail:
        if await self._repository.find_by_slug(str(request.slug)):
            raise CategorySlugAlreadyExistsException(str(request.slug))

        category = Category(
            name=request.name,
            slug=str(request.slug),
            description=request.description,
            color=request.color,
            created_by=actor_public_id,
            updated_by=actor_public_id,
        )
        saved = await self._repository.save(category)
        await self._uow.commit()
        return CategoryMapper.to_detail(saved)