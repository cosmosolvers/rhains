from typing import Any, Optional, Callable

from ..field import Field

from exceptions.core.models import field


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

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and all(char in "0123456789ABCDEF" for char in value)
