from typing import Any, Callable

from .field import Field

from exception.core.models import field


class TextField(Field):
    """
    TEXT FIELD
    ==========
    champ de texte

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise TextFieldDefaultError: si la valeur par defaut n'est pas valide

    :return: str
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
        default = default if default and not callable(default) else default()
        if default and not isinstance(default, str):
            raise field.TextFieldDefaultError(f"{default} is not a valid default value")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and isinstance(value, str)
