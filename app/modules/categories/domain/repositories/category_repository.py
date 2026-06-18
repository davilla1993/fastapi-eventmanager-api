from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.categories.domain.entities.category import Category


class AbstractCategoryRepository(ABC):
    @abstractmethod
    async def find_by_public_id(self, public_id: UUID) -> Category | None: ...

    @abstractmethod
    async def find_by_slug(self, slug: str) -> Category | None: ...

    @abstractmethod
    async def find_all(
        self, offset: int, limit: int
    ) -> tuple[list[Category], int]: ...

    @abstractmethod
    async def save(self, category: Category) -> Category: ...

    @abstractmethod
    async def delete(self, category: Category) -> None: ...