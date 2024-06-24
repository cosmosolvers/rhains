from typing import Any, Optional, Callable

from ..field import Field

from exception.core.models import field

from utils.bin import (
    base32_to_decimal,
    base32_to_binary,
    base32_to_hexadecimal,
    base32_to_base64,
    base32_to_base64url,
    base32_to_baseN
)


basen = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"


class Base32Field(Field):
    """
    BASE32 FIELD
    ============

    champ de nombres en base32

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
        if default and not all(char in basen for char in default):
            raise field.FieldDefaultError("default value must be base32")

        super().__init__(nullable, default, primary_key, unique, editable, check)

    def to_decimal(self) -> int:
        return base32_to_decimal(self._value)

    def to_hexadecimal(self) -> str:
        return base32_to_hexadecimal(self._value)

    def to_binary(self) -> str:
        return base32_to_binary(self._value)

    def to_base64(self) -> str:
        return base32_to_base64(self._value)

    def to_base64url(self) -> str:
        return base32_to_base64url(self._value)

    def to_baseN(self, base: int) -> str:
        return base32_to_baseN(self._value, base)

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and all(char in basen for char in value)
