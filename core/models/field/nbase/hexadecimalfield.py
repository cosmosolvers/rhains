from typing import Any, Optional, Callable

from ..field import Field

from exception.core.models import field

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
    nombres hexadecimal
    """

    def __init__(
            self,
            max_length: int,
            nullable: bool = True,
            default: Optional[str] = None,
            primary_key: bool = False,
            unique: bool = False,
            editable: bool = True,
            check: Optional[Callable] = None,
    ):
        self._max_length = max_length
        if default and len(default) > max_length:
            raise field.FieldDefaultError("default value is too long")
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

    def _validated(self, value: Any) -> bool:
        if len(value) > self._max_length:
            return False
        return super()._validated(value) and all(char in "0123456789ABCDEF" for char in value)
