from typing import Any, List, Tuple, Optional
import json

from ..field import Field


class ArrayField(Field):
    """
    ARRAY FIELD
    ===========
    champ de listes et les tuples

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param editable: valeur editable
    :param check: fonction de validation

    :return: List[Any] | Tuple[Any]
    """

    def __init__(
            self,
            nullable: bool = True,
            default: Optional[List[Any] | Tuple[Any]] = None,
            editable: bool = True,
            check: Optional[Any] = None,
    ):
        super().__init__(
            nullable=nullable,
            default=default,
            editable=editable,
            check=check
        )

    def load(self, value: Any) -> Any:
        return json.loads(value)

    def dump(self, value) -> str:
        return json.dumps(value)

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and isinstance(value, (list, tuple))
