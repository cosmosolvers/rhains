from typing import Any, Callable
from os import path

from ..field import Field

from exceptions.core.models import field


class FilePathField(Field):
    """
    FILE PATH FIELD
    ===============
    champ de chamin de fichier

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary key: cle primaire
    :param unique: valuer unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise FilePathFieldTypeError: si la valeur n'est pas un str
    :raise FilePathValueError: si la value n'est pas un path (ne contient pas '/')

    :return: path
    """

    def __init__(
        self,
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if default:
            if not isinstance(default, str):
                raise field.FilePathFieldTypeError(f"{default} not str")
            if '/' not in default:
                raise field.FilePathValueError(f'{default} not is path')
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: Any) -> Any:
        return path(value)

    def dump(self) -> Any:
        return str(self._value)

    def _validated(self, value: str) -> bool:
        if value:
            if not isinstance(value, str):
                raise field.FilePathFieldTypeError(f"{value} not str")
            if '/' not in value:
                raise field.FilePathValueError(f'{value} not is path')
        return super()._validated(value)
