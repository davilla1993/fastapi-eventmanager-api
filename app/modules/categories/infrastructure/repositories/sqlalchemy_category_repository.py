from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.categories.domain.entities.category import Category
from app.modules.categories.domain.repositories.category_repository import (
    AbstractCategoryRepository,
)


class SqlAlchemyCategoryRepository(AbstractCategoryRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_public_id(self, public_id: UUID) -> Category | None:
        result = await self._session.execute(
            select(Category).where(
                Category.public_id == public_id, Category.deleted.is_(False)
            )
        )
        return result.scalar_one_or_none()

    async def find_by_slug(self, slug: str) -> Category | None:
        result = await self._session.execute(
            select(Category).where(
                Category.slug == slug, Category.deleted.is_(False)
            )
        )
        return result.scalar_one_or_none()

    async def find_all(self, offset: int, limit: int) -> tuple[list[Category], int]:
        base = select(Category).where(Category.deleted.is_(False))
        total_result = await self._session.execute(
            select(func.count()).select_from(base.subquery())
        )
        total: int = total_result.scalar_one()
        items_result = await self._session.execute(
            base.order_by(Category.name).offset(offset).limit(limit)
        )
        return list(items_result.scalars().all()), total

    async def save(self, category: Category) -> Category:
        self._session.add(category)
        await self._session.flush()
        await self._session.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        category.deleted = True
        self._session.add(category)
        await self._session.flush()