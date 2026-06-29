from app.modules.iam.api.dto.responses.auth_responses import UserResponse
from app.modules.iam.domain.repositories.user_repository import AbstractUserRepository
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams


class ListUsersUseCase:
    def __init__(self, repository: AbstractUserRepository) -> None:
        self._repository = repository

    async def execute(self, pagination: PaginationParams) -> PaginatedResponse[UserResponse]:
        users, total = await self._repository.list_all(
            offset=pagination.offset, limit=pagination.size
        )
        return PaginatedResponse.create(
            items=[UserResponse.model_validate(u) for u in users],
            total=total,
            page=pagination.page,
            size=pagination.size,
        )