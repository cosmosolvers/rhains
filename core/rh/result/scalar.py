""""""
from typing import Dict

from .result import RhesultOne, RhesultMany

from exception.core.rh.database import rhesult as rhs


class Vector(RhesultOne):
    def __init__(self, collection, **kwargs) -> None:
        super().__init__(collection, **kwargs)
        if kwargs and len(kwargs) > 0:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def _to_dict(self) -> Dict:
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }


class VectorList(RhesultMany):
    def _validate(self, item):
        if not isinstance(item, Vector):
            raise rhs.RhesultDataTypeError(f"Expected Vector, got {type(item)}")
