from typing import Any, List, Tuple, Optional, Callable, Dict
import json

from ..field import Field

from exceptions.core.models import field
from utils.validefunc import validate_function


class AggregationField(Field):
    """
    AGGREGATION FIELD
    =================
    operation d'aggregation

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param editable: valeur editable
    :param check: fonction de validation
    :param functions: fonctions d'aggregation

    :raise FieldFunctionError: si la fonction n'est pas valide

    :return: List[Tuple] | Tuple[Tuple]
    """

    def __init__(
            self,
            nullable: bool = True,
            default: Optional[List[Tuple] | Tuple[Tuple]] = None,
            editable: bool = True,
            check: Optional[Any] = None,
            functions: Optional[Dict[str, Callable]] = None
    ):
        if functions:
            for k, v in functions.items():
                if not validate_function(v):
                    raise field.FieldFunctionError(f"{v} is not a valid function")
                setattr(self, k, self._wrap_function(v))

        super().__init__(
            nullable=nullable,
            default=default,
            editable=editable,
            check=check
        )

    def load(self, value: Any) -> Any:
        return [tuple(item) for item in tuple(json.loads(value))]

    def dump(self, value: List[Tuple] | Tuple[Tuple]) -> str:
        return json.dumps(value)

    def _wrap_function(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    def _validated(self, value: Any) -> bool:
        if not isinstance(value, (list, tuple)):
            raise field.AggregationFieldValueError(f'{value} must be tuple list or tuple of tuple')
        for item in value:
            if not isinstance(item, tuple):
                raise field.AggregationFieldValueError(f'{item} must be tuple')
        return super()._validated(value)
