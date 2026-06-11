class AppException(Exception):
    status_code: int = 500

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    status_code = 404

    def __init__(self, resource: str, identifier: str | int) -> None:
        super().__init__(f"{resource} '{identifier}' introuvable.")


class ConflictException(AppException):
    status_code = 409


class UnauthorizedException(AppException):
    status_code = 401

    def __init__(self, message: str = "Non authentifié.") -> None:
        super().__init__(message)


class ForbiddenException(AppException):
    status_code = 403

    def __init__(self, message: str = "Accès refusé.") -> None:
        super().__init__(message)


class UnprocessableEntityException(AppException):
    status_code = 422
