
from typing import Any, Callable, Optional, List

from ..field import Field

from exceptions.core.models import field

from utils.bin import (
    str_to_base32,
    str_to_base64,
    str_to_base64url,
    str_to_decimal,
    str_to_hexadecimal,
    str_to_binary
)


class CharField(Field):
    """
    CHARFIELD
    =========
    champ de str

    :param max_length: longueur maximale
    :param min_length: longueur minimale
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation
    :param choices: liste des valeurs autorisées

    :raise CharFieldMaxLengthError: si la valeur est trop longue
    :raise CharFieldMinLengthError: si la valeur est trop courte
    :raise CharFieldMinMaxLengthError: si la longueur minimale est superieure a la longueur maximale
    :raise CharFieldChoicesError: si la valeur n'est pas dans les choix

    :return: str
    """

    def __init__(
        self,
        max_length: int,
        min_length: Optional[int] = None,
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None,
        choices: Optional[List[str]] = None
    ):
        self._max_length = max_length
        if default and len(default) > self._max_length:
            raise field.CharFieldMaxLengthError(f'{default} too long')

        self._min_length = min_length
        if self._min_length and self._min_length > self._max_length:
            raise field.CharFieldMinLengthError(f'{self._min_length} > {self._max_length}')

        if self._min_length and default and len(default) < self._min_length:
            raise field.CharFieldMinLengthError(f'{default} too short')

        if choices and default and default not in choices:
            raise field.CharFieldChoicesError(f'{default} not in choices')

        self._choices = choices if choices and all(
            isinstance(h, str) and len(h) <= self._max_length for h in choices) else None

        if self._min_length and self._choices and any(
            len(h) < self._min_length for h in self._choices
        ):
            raise field.CharFieldMinLengthError(f'{self._choices} too short')

        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def to_base32(self) -> str:
        return str_to_base32(self._value)

    def to_base64(self) -> str:
        return str_to_base64(self._value)

    def to_base64url(self) -> str:
        return str_to_base64url(self._value)

    def to_decimal(self) -> int:
        return str_to_decimal(self._value)

    def to_hexadecimal(self) -> str:
        return str_to_hexadecimal(self._value)

    def to_binary(self) -> str:
        return str_to_binary(self._value)

    def _validated(self, value: Any) -> bool:
        if self._choices and value not in self._choices:
            raise field.CharFieldChoicesError(f'{value} not in choices')
        if len(value) > self._max_length:
            raise field.CharFieldMaxLengthError(f'{value} too long')
        if self._min_length and self._min_length > self._max_length:
            raise field.CharFieldMinLengthError(f'{self._min_length} > {self._max_length}')
        if self._min_length and len(value) < self._min_length:
            raise field.CharFieldMinLengthError(f'{value} too short')
        return super()._validated(value)
