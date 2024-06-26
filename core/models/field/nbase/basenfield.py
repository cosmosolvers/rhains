from typing import Any, Optional, Callable

from ..field import Field

from exceptions.core.models import field

from utils.bin import (
    baseN_to_decimal,
    baseN_to_binary,
    baseN_to_hexadecimal,
    baseN_to_base64,
    baseN_to_base64url,
    baseN_to_base32,
)


baseno = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


class BaseNField(Field):
    """
    BASEN FIELD
    ===========
    champ de nombres en baseN

    :param base: base du nombre
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise FieldBaseError: si la base n'est pas valide
    :raise FieldDefaultError: si la valeur par defaut n'est pas valide

    :return: str
    """

    def __init__(
            self,
            base: int,
            nullable: bool = True,
            default: Optional[str] = None,
            primary_key: bool = False,
            unique: bool = False,
            editable: bool = True,
            check: Optional[Callable] = None,
    ):
        self._base = base
        if self._base < 2 or self._base > 62:
            raise field.FieldBaseError("base must be between 2 and 62")
        if default and not all(char in baseno[:base] for char in default):
            raise field.FieldDefaultError(f"default value must be base{base}")

        super().__init__(nullable, default, primary_key, unique, editable, check)

    def to_decimal(self) -> int:
        return baseN_to_decimal(self._value, self._base)

    def to_hexadecimal(self) -> str:
        return baseN_to_hexadecimal(self._value, self._base)

    def to_binary(self) -> str:
        return baseN_to_binary(self._value, self._base)

    def to_base64(self) -> str:
        return baseN_to_base64(self._value, self._base)

    def to_base64url(self) -> str:
        return baseN_to_base64url(self._value, self._base)

    def to_base32(self) -> str:
        return baseN_to_base32(self._value, self._base)

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and all(char in baseno[:self._base] for char in value)
