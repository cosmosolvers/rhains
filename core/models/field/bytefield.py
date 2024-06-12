from typing import Any, Callable

from .field import Field

from exception.core.models import field


class ByteField(Field):
    """
    BYTES FIELD
    ===========
    champ de bytes

    :param max_length: longueur maximale
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise BytesFieldValueError: si la valeur n'est pas valide
    :raise ByteFieldOvervalueError: si la valeur est trop longue

    :return: bytes
    """

    def __init__(
        self,
        max_length: int,
        nullable: bool = True,
        default: str | bytes | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if not isinstance(max_length, int):
            raise field.IntegerValueError(f"{max_length} must be int")

        self._max_length = max_length
        if default and not isinstance(default, (str, bytes)):
            raise field.BytesFieldValueError(f"{default} must be str or bytes")

        if default:
            default = default.encode('utf-8') if isinstance(default, str) else default
            if len(default) > self._max_length:
                raise field.ByteFieldOvervalueError(f'{default} is too long')

        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def __set__(self, instance, value):
        if isinstance(value, str):
            value = value.encode('utf-8')
        return super().__set__(instance, value)

    def load(self, value: str) -> bytes:
        return value.encode('utf-8')

    def dump(self) -> str:
        return self._value.decode('utf-8')

    def _validated(self, value: str | bytes) -> bool:
        if not isinstance(value, (int, str)):
            raise field.BytesFieldValueError(f"{value} must be str or bytes")
        return super()._validated(value)
