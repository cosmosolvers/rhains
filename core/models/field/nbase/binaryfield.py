from typing import Any, Optional, Callable

from ..field import Field

from utils.bin import (
    binary_to_decimal,
    binary_to_hexadecimal,
    binary_to_base64,
    binary_to_base64url,
    binary_to_base32,
    binary_to_baseN
)
# exception class
from exception.core.models import field


class BinaryField(Field):
    """
    BINARY FIELD
    ============
    champ de nombres en binaire

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
            default: Optional[int] = None,
            primary_key: bool = False,
            unique: bool = False,
            editable: bool = True,
            check: Optional[Callable] = None,
    ):
        if default and all(char in "01" for char in default):
            raise field.FieldDefaultError("default value must be binary")

        super().__init__(nullable, default, primary_key, unique, editable, check)

    def to_decimal(self) -> int:
        return binary_to_decimal(self._value)

    def to_hexadecimal(self) -> str:
        return binary_to_hexadecimal(self._value)

    def to_base64(self) -> str:
        return binary_to_base64(self._value)

    def to_base64url(self) -> str:
        return binary_to_base64url(self._value)

    def to_base32(self) -> str:
        return binary_to_base32(self._value)

    def to_baseN(self, base: int) -> str:
        return binary_to_baseN(self._value, base)

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and all(char in "01" for char in value)
