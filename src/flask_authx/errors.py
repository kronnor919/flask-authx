class ProgrammingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class AppError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ConfigurationError(AppError):
    pass


class NotFoundError(AppError):
    pass


class ValidationError(AppError):
    pass


class DatabaseError(AppError):
    pass


class ConflictError(AppError):
    pass


class DependentResourceError(AppError):
    pass


class NotAuthenticatedError(AppError):
    pass


class InvalidCredentialsError(AppError):
    pass
