"""
type de rendu des données a leurs sortie de la base de donnée

$push, $get, $set => RhesultOne | None
$pull => RhesultMany
"""
import json
from typing import Iterable

from exception.core.rh.database import rhesult as rhs


class Rhesult:
    def __init__(self, collection, **kwargs) -> None:
        self._instruct, self._tablename = collection.instruct

    def _to_json(self) -> str:
        return json.dumps(self._to_dict())


class RhesultOne(Rhesult):

    def delete(self):
        self._instruct.delete(self._tablename, self.pk)

    def save(self):
        return self._connexion.update(self.pk, **self._to_dict())

    def update(self, **kwargs):
        return self._connexion.update(self.pk, **kwargs)

    @property
    def json(self):
        return self._to_json()


class RhesultMany:
    def __init__(self, collection, *args):
        self._instruct, self._tablename = collection.instruct
        self._data = []
        for item in args:
            if self._validate(item):
                self._data.append(item)

    def collect(self, **kwargs):
        if kwargs and len(kwargs) == 1:
            key, value = kwargs.popitem()
            if key == '$.':
                return self._point_collect(value)
            if key == '$sort':
                return self._sort_collect(value)
            if key == '$-':
                return self._many_collect(value)
            if key == '$':
                return self._many_collect(value)
        return self._data

    def append(self, object) -> None:
        self._validate(object)
        self._data.append(object)

    def extend(self, iterable: Iterable) -> None:
        for item in iterable:
            self._validate(item)
        self._data.extend(iterable)

    def insert(self, index: int, object: RhesultOne | None) -> None:
        self._validate(object)
        self._data.insert(index, object)

    # def __iadd__(self, value) -> Self:
    #     for item in value:
    #         self._validate(item)
    #     return

    # def __setitem__(self, index, object):
    #     if isinstance(index, slice):
    #         for item in object:
    #             self._validate(item)
    #     else:
    #         self._validate(object)

    def _sort_collect(self, data):
        pass

    def _exclude_collect(self, data):
        if not isinstance(data, dict):
            raise rhs.RhesultDataTypeError(f"{data} must be dict")
        k, v = data.popitem()
        for i in self._data:
            if getattr(i, k) == v:
                self._data.remove(i)
        return self._data

    def _many_collect(self, data):
        if not isinstance(data, list):
            raise rhs.RhesultDataTypeError(f"{data} must be list")
        exclude = data.get('$-')
        if exclude:
            self._data = self.collect(**data)
        sort = data.get('$sort')
        if sort:
            self._data = self.collect(**data)
        other = data.get('$.')
        if other:
            self._data = self.collect(**data)
        return self._data

    def _point_collect(self, data):
        if data == '*':
            return self._data
        if data == '!':
            return len(self._data) > 0
        if data == '?':
            return len(self._data)
        if data in ('0', 0):
            return self._data[0]
        if data == -1:
            return self._data[-1]
        if isinstance(data, tuple):
            return self._tuple_collect(data)

    def _tuple_collect(self, data):
        if len(data) != 2:
            raise rhs.RhesultDataTypeError(f"{data} must be 2 arguments")
        offset, limit = data
        if not isinstance(offset, int):
            raise rhs.RhesultDataTypeError(f"{offset} must be int")
        if offset < 0:
            raise rhs.RhesultDataTypeError(f"{offset} must be positive")
        if not isinstance(limit, int):
            raise rhs.RhesultDataTypeError(f"{limit} must be int")
        if limit < 0:
            raise rhs.RhesultDataTypeError(f"{limit} must be positive")
        if limit == 0:
            return self._data[offset:]
        else:
            return self._data[offset:limit]

    def _validate(self, item):
        if not isinstance(item, RhesultOne):
            raise rhs.RhesultDataTypeError(f"Expected RhesultOne, got {type(item)}")


class Success:
    pass


class Fails:
    pass


# essayer de retraduire les donn"e en Model avant de les envoyer en Rhesult
# afin d'avoir plus de possibilité d'action
# comme les tri en verifiant si la donnée est triable
# en faisant les trie en fonction des champ sur les foreignkeys
# et plus encore
