from typing import Any, List, Tuple, Optional, Callable
import json

from .field import Field


class ArrayField(Field):
    """
    ARRAY FIELD
    ===========
    field pour les listes et les tuples
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

    def dump(self) -> str:
        return json.dumps(self._value)

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
