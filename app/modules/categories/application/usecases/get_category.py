from uuid import UUID

from app.modules.categories.api.dto.responses.category_responses import (
    CategoryReadDetail,
)
from app.modules.categories.application.mappers.category_mapper import CategoryMapper
from app.modules.categories.domain.exceptions.category_exceptions import (
    CategoryNotFoundException,
)
from app.modules.categories.domain.repositories.category_repository import (
    AbstractCategoryRepository,
)


class GetCategoryUseCase:
    def __init__(self, repository: AbstractCategoryRepository) -> None:
        self._repository = repository

    async def execute(self, public_id: UUID) -> CategoryReadDetail:
        category = await self._repository.find_by_public_id(public_id)
        if not category:
            raise CategoryNotFoundException(str(public_id))
        return CategoryMapper.to_detail(category)