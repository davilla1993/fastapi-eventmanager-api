from app.shared.exceptions.base import AppException


class EventNotFoundException(AppException):
    status_code = 404

    def __init__(self, identifier: str) -> None:
        super().__init__(f"Événement '{identifier}' introuvable.")


class EventSlugAlreadyExistsException(AppException):
    status_code = 409

    def __init__(self, slug: str) -> None:
        super().__init__(f"Un événement avec le slug '{slug}' existe déjà.")


class EventDateRangeException(AppException):
    status_code = 422

    def __init__(self) -> None:
        super().__init__("La date de fin doit être postérieure à la date de début.")