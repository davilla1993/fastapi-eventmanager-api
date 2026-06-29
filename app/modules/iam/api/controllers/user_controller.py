from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.session import get_db
from app.infrastructure.security.dependencies import require_admin
from app.modules.iam.api.dto.responses.auth_responses import UserResponse
from app.modules.iam.application.usecases.list_users import ListUsersUseCase
from app.modules.iam.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)
from app.shared.pagination.schemas import PaginatedResponse, PaginationParams

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=PaginatedResponse[UserResponse],
    summary="Lister tous les utilisateurs",
    description="Retourne la liste paginée de tous les comptes utilisateurs. **Réservé aux ADMINs.**",
    response_description="Liste paginée d'utilisateurs.",
)
async def list_users(
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
    _: object = Depends(require_admin),
) -> PaginatedResponse[UserResponse]:
    repo = SqlAlchemyUserRepository(db)
    return await ListUsersUseCase(repo).execute(pagination)