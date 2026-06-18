from app.modules.categories.api.dto.responses.category_responses import CategoryRead
from app.modules.categories.application.mappers.category_mapper import CategoryMapper
from app.modules.categories.domain.repositories.category_repository import (
    AbstractCategoryRepository,
)
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams


class ListCategoriesUseCase:
    def __init__(self, repository: AbstractCategoryRepository) -> None:
        self._repository = repository

    async def execute(
        self, pagination: PaginationParams
    ) -> PaginatedResponse[CategoryRead]:
        categories, total = await self._repository.find_all(
            offset=pagination.offset, limit=pagination.size
        )
        return PaginatedResponse.create(
            items=[CategoryMapper.to_read(c) for c in categories],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )