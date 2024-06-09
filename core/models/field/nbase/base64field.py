from typing import Any, Optional, Callable

from ..field import Field

from exception.core.models import field

from utils.bin import (
    base64_to_base32,
    base64_to_baseN,
    base64_to_decimal,
    base64_to_hexadecimal,
    base64_to_binary,
    base64_to_base64url
)


basexs = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+/"


class Base64Field(Field):
    """
    BASE64 FIELD
    ============
    nombres base64
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
        if default and not all(char in basexs for char in default):
            raise field.FieldDefaultError("default value must be base64")

        super().__init__(nullable, default, primary_key, unique, editable, check)

    def to_decimal(self) -> int:
        return base64_to_decimal(self._value)

    def to_hexadecimal(self) -> str:
        return base64_to_hexadecimal(self._value)

    def to_binary(self) -> str:
        return base64_to_binary(self._value)

    def to_base64url(self) -> str:
        return base64_to_base64url(self._value)

    def to_base32(self) -> str:
        return base64_to_base32(self._value)

    def to_baseN(self, base: int) -> str:
        return base64_to_baseN(self._value, base)

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and all(char in basexs for char in value)
