from ..field import Field

from exceptions.core.models import field
from typing import Any, Optional, Callable
import json


class MatrixField(Field):
    """
    MATRIX FIELD
    ============
    Champ pour stocker et manipuler des matrices

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise MatrixFieldError: si la valeur par defaut n'est pas valide
    :raise FieldNullableError: si la valeur est nulle et non autorisée

    :return: list[list[Any]]
    """

    def __init__(
        self,
        nullable: bool = True,
        default: Optional[list[list[Any]]] = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if default:
            if not self._validated_matrix(default):
                raise field.MatrixFieldError(f"{default} is not a valid matrix")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def _validated_matrix(self, value: Any) -> bool:
        if isinstance(value, list):
            if all(isinstance(i, list) for i in value):
                return True
        return False

    def load(self, value: str) -> list[list[Any]]:
        return json.loads(value)

    def dump(self) -> str:
        return json.dumps(self._value)

    def _validated(self, value: Any) -> bool:
        return self._validated_matrix(value) and super()._validated(value)
