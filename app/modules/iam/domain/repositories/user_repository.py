from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.iam.domain.entities.user import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def find_by_public_id(self, public_id: UUID) -> User | None: ...

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def list_all(self, offset: int = 0, limit: int = 20) -> tuple[list[User], int]: ...
