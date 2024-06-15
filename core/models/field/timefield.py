from typing import Any, Callable
from datetime import time

from .field import Field

from exception.core.models import field


class TimeField(Field):
    """
    TIME FIELD
    ==========
    champ de temps

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise TimeFieldDefaultError: si la valeur par defaut n'est pas valide

    :return: time
    """

    def __init__(
        self,
        format: str = ['%H:%M:%S'],
        nullable: bool = True,
        default: Any | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        default = default if default and not callable(default) else default()
        if default and not isinstance(default, time):
            raise field.TimeFieldDefaultError(f"{default} is not a valid default value")
        default = default.strftime(format)
        self._format = format
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: str) -> time:
        return time.fromisoformat(value)

    def dump(self) -> time:
        return self._value.strftime(self._format[0])

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and isinstance(value, time)
