from typing import Any, Optional, Callable

from ..field import Field

from exceptions.core.models import field

from utils.bin import (
    hexadecimal_to_decimal,
    hexadecimal_to_binary,
    hexadecimal_to_base64,
    hexadecimal_to_base64url,
    hexadecimal_to_base32,
    hexadecimal_to_baseN,
)


class HexadecimalField(Field):
    """
    HEXADECIMAL FIELD
    =================
    champ de nombres en hexadecimal

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise FieldDefaultError: si la valeur par defaut n'est pas valide

    :return: str
    """

    def __init__(
            self,
            nullable: bool = True,
            default: Optional[str] = None,
            primary_key: bool = False,
            unique: bool = False,
            editable: bool = True,
            check: Optional[Callable] = None,
    ):
        if default and all(char in "0123456789ABCDEF" for char in default):
            raise field.FieldDefaultError("default value must be hexadecimal")

        super().__init__(nullable, default, primary_key, unique, editable, check)

    def to_decimal(self) -> int:
        return hexadecimal_to_decimal(self._value)

    def to_binary(self) -> str:
        return hexadecimal_to_binary(self._value)

    def to_base64(self) -> str:
        return hexadecimal_to_base64(self._value)

    def to_base64url(self) -> str:
        return hexadecimal_to_base64url(self._value)

    def to_base32(self) -> str:
        return hexadecimal_to_base32(self._value)

    def to_baseN(self, base: int) -> str:
        return hexadecimal_to_baseN(self._value, base)

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and all(char in "0123456789ABCDEF" for char in value)
