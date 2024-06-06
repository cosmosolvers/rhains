""""""
import json
from _collections_abc import dict_keys

from .result import RhesultOne, RhesultMany

from exception.core.rh.database import rhesult as rhs


class StoredKey(RhesultOne):
    def __init__(self, collection, **kwargs) -> None:
        super().__init__(collection, **kwargs)
        self._data = {}
        for key, value in kwargs.items():
            self.data[key] = value

    def _to_json(self) -> str:
        return json.dumps(self)

    def __setitem__(self, key, value):
        self._data['key'] = value

    def __getitem__(self, key: str):
        if key not in self._data.keys():
            raise rhs.StoredKeyFieldError(f"{key} not found")
        return self._rhconn.get(key)

    def __delitem__(self, key: str):
        if key not in self._data.keys():
            raise rhs.StoredKeyFieldError(f"{key} not found")

    def keys(self) -> dict_keys:
        return self._data.keys()

    def values(self) -> dict_keys:
        return self._data.values()

    def items(self) -> dict_keys:
        return self._data.items()


class StoredKeyList(RhesultMany):
    def _validate(self, item):
        if not isinstance(item, StoredKey):
            raise rhs.RhesultDataTypeError(f"Expected StoredKey, got {type(item)}")
