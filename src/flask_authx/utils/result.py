from dataclasses import dataclass

from flask_authx.domain.errors import ProgrammingError


@dataclass
class Result[T, E]:
    _success: bool
    _value: T | None
    _error: E | None

    @staticmethod
    def ok[U, F](value: U) -> "Result[U, F]":  # type: ignore
        return Result[U, F](True, value, None)

    @staticmethod
    def fail[U, F](error: F) -> "Result[U, F]":  # type: ignore
        return Result[U, F](False, None, error)

    def error_is(self, error_type: type[E]) -> bool:
        return isinstance(self._error, error_type)

    @property
    def value(self) -> T:
        if self._value is None:
            raise ProgrammingError(
                "Cannot obtain 'value' property from NOT successful result."
            )
        return self._value

    @property
    def error(self) -> E:
        if self._error is None:
            raise ProgrammingError(
                "Cannot obtain 'error' property from successful result."
            )
        return self._error

    @property
    def success(self) -> bool:
        return self._success
