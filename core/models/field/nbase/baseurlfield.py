from typing import Any, Optional, Callable

from ..field import Field

from exceptions.core.models import field

from utils.bin import (
    base64url_to_decimal,
    base64url_to_binary,
    base64url_to_hexadecimal,
    base64url_to_base64,
    base64url_to_base32,
    base64url_to_baseN,
)


baseurl = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


class Base64UrlField(Field):
    """
    BASE64URL FIELD
    ===============
    chmap de nombres en base64url

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
        if default and not all(char in baseurl for char in default):
            raise field.FieldDefaultError("default value must be base64url")

        super().__init__(nullable, default, primary_key, unique, editable, check)

    def to_decimal(self) -> int:
        return base64url_to_decimal(self._value)

    def to_hexadecimal(self) -> str:
        return base64url_to_hexadecimal(self._value)

    def to_binary(self) -> str:
        return base64url_to_binary(self._value)

    def to_base64(self) -> str:
        return base64url_to_base64(self._value)

    def to_base32(self) -> str:
        return base64url_to_base32(self._value)

    def to_baseN(self, base: int) -> str:
        return base64url_to_baseN(self._value, base)

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and all(char in baseurl for char in value)
