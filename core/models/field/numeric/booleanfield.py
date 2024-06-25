from typing import Any

from ..field import Field
# exception class
from exception.core.models import field


class BooleanField(Field):
    """
    BOOLEAN FIELD
    =============
    champ booleen True (1) False (0)

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param editable: valeur editable

    :raise BooleanFieldValueError: si la valeur par defaut n'est pas valide
    :raise FieldDefaultError: si la valeur par defaut n'est pas valide

    :return: int
    """

    def __init__(
        self,
        nullable: bool = True,
        default: int | bool | None = None,
        editable: bool = True
    ):
        if default and default not in (True, False, 0, 1):
            raise field.BooleanFieldValueError(f"{default} is invalid")
        self._default = default
        super().__init__(
            nullable=nullable,
            default=self._default,
            editable=editable
        )

    def __set__(self, instance, value):
        if value in (True, 1):
            value = 1
        if value in (False, 0):
            value = 0
        return super().__set__(instance, value)

    def load(self, value: Any) -> int:
        return int(value)

    def dump(self) -> int:
        return 1 if self._value in (True, 1) else 0

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and value in (True, False, 1, 0)
