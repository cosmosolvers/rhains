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
    nombres binaire
    """

    def __init__(
            self,
            max_length: int,
            nullable: bool = True,
            default: Optional[int] = None,
            primary_key: bool = False,
            unique: bool = False,
            editable: bool = True,
            check: Optional[Callable] = None,
    ):
        self._max_length = max_length
        if default and len(default) > max_length:
            raise field.FieldDefaultError("default value is too long")
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

    def _validated(self, value: Any) -> bool:
        if len(value) > self._max_length:
            return False
        return super()._validated(value) and all(char in "01" for char in value)
