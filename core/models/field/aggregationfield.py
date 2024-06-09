from typing import Any, List, Tuple, Optional, Callable, Dict
import inspect
import json

from .field import Field

from exception.core.models import field


class AggregationField(Field):
    """
    AGGREGATION FIELD
    =================
    operation d'aggregation
    """

    def __init__(
            self,
            nullable: bool = True,
            default: Optional[List[Tuple] | Tuple[Tuple]] = None,
            editable: bool = True,
            check: Optional[Any] = None,
            functions: Optional[Dict[str, Callable]] = None
    ):
        for k, v in functions.items():
            if not self._validate_function(v):
                raise field.FieldFunctionError(f"{v} is not a valid function")
            setattr(self, k, self._wrap_function(v))

        super().__init__(
            nullable=nullable,
            default=default,
            editable=editable,
            check=check
        )

    def load(self, value: Any) -> Any:
        return json.loads(value)

    def dump(self) -> str:
        return json.dumps(self._value)

    def _validate_function(self, func: Callable) -> bool:
        signature = inspect.signature(func)
        return len(signature.parameters) > 0 and next(iter(signature.parameters)).name == 'args'

    def _wrap_function(self, func: Callable) -> Callable:
        def wrapper():
            return func(*self._value)
        return wrapper

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and isinstance(value, (List, Tuple))

    def __contains__(self, item: Any) -> bool:
        return item in self._value

    def __getitem__(self, item: int) -> Any:
        return self._value[item]

    def __len__(self) -> int:
        return len(self._value)

    def __iter__(self) -> Any:
        return iter(self._value)

    def __reversed__(self) -> Any:
        return reversed(self._value)

    def __add__(self, other: Any) -> Any:
        self._validated(other)
        return self._value + other

    def __sub__(self, other: Any) -> Any:
        self._validated(other)
        return self._value - other

    def append(self, value: Any) -> None:
        self._validated(value)
        self._value.append(value)

    def clear(self) -> None:
        self._value.clear()

    def copy(self) -> Any:
        return self._value.copy()

    def count(self, value: Any) -> int:
        return self._value.count(value)

    def extend(self, value: Any) -> None:
        self._validated(value)
        self._value.extend(value)

    def index(self, value: Any) -> int:
        return self._value.index(value)

    def insert(self, index: int, value: Any) -> None:
        self._validated(value)
        self._value.insert(index, value)

    def pop(self, index: int) -> Any:
        return self._value.pop(index)

    def remove(self, value: Any) -> None:
        self._value.remove(value)

    def reverse(self) -> None:
        self._value.reverse()

    def sort(self, key: Optional[Callable] = None, reverse: bool = False) -> None:
        self._value.sort(key=key, reverse=reverse)
