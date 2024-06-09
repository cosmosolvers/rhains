
from typing import Any, Callable

from .field import Field

from exception.core.models import field


class CharField(Field):
    """
    CHARFIELD
    =========
    str field
    """

    def __init__(
        self,
        max_length: str,
        nullable: bool = True,
        default: Any | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )
        self._max_length = max_length
        if self._default and len(self._default) > self._max_length:
            raise field.CharFieldMaxLengthError(f'{self._default} too long')

    def load(self, value: Any) -> Any:
        return value

    def dump(self) -> Any:
        return self._value

    def _validated(self, value: Any) -> bool:
        if len(value) != self._max_length:
            raise field.CharFieldMaxLengthError(f'{value} too long')
        return super()._validated(value)
