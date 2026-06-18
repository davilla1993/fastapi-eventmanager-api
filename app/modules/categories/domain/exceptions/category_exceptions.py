from app.shared.exceptions.base import AppException


class CategoryNotFoundException(AppException):
    status_code = 404

    def __init__(self, identifier: str) -> None:
        super().__init__(f"Catégorie '{identifier}' introuvable.")


class CategorySlugAlreadyExistsException(AppException):
    status_code = 409

    def __init__(self, slug: str) -> None:
        super().__init__(f"Une catégorie avec le slug '{slug}' existe déjà.")