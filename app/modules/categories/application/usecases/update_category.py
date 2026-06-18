from uuid import UUID

from app.modules.categories.api.dto.requests.category_requests import CategoryUpdate
from app.modules.categories.api.dto.responses.category_responses import (
    CategoryReadDetail,
)
from app.modules.categories.application.mappers.category_mapper import CategoryMapper
from app.modules.categories.domain.exceptions.category_exceptions import (
    CategoryNotFoundException,
    CategorySlugAlreadyExistsException,
)
from app.modules.categories.domain.repositories.category_repository import (
    AbstractCategoryRepository,
)
from app.shared.domain.unit_of_work import UnitOfWork


class UpdateCategoryUseCase:
    def __init__(
        self, repository: AbstractCategoryRepository, uow: UnitOfWork
    ) -> None:
        self._repository = repository
        self._uow = uow

    async def execute(
        self, public_id: UUID, request: CategoryUpdate, actor_public_id: UUID
    ) -> CategoryReadDetail:
        category = await self._repository.find_by_public_id(public_id)
        if not category:
            raise CategoryNotFoundException(str(public_id))

        if request.slug is not None and str(request.slug) != category.slug:
            if await self._repository.find_by_slug(str(request.slug)):
                raise CategorySlugAlreadyExistsException(str(request.slug))
            category.slug = str(request.slug)

        if request.name is not None:
            category.name = request.name
        if request.description is not None:
            category.description = request.description
        if request.color is not None:
            category.color = request.color

        category.updated_by = actor_public_id
        saved = await self._repository.save(category)
        await self._uow.commit()
        return CategoryMapper.to_detail(saved)