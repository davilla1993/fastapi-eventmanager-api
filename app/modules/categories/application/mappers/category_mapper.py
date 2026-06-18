from app.modules.categories.api.dto.responses.category_responses import (
    CategoryRead,
    CategoryReadDetail,
)
from app.modules.categories.domain.entities.category import Category


class CategoryMapper:
    @staticmethod
    def to_read(category: Category) -> CategoryRead:
        return CategoryRead.model_validate(category)

    @staticmethod
    def to_detail(category: Category) -> CategoryReadDetail:
        return CategoryReadDetail.model_validate(category)