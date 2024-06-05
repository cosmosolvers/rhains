""""""
from typing import Iterable, Dict, Self, Any
import json


class Rhesult:
    def __init__(self, connexion, **kwargs) -> None:
        self._instruct, self._tablename = connexion.instruct

        if kwargs and len(kwargs) > 0:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def _to_dict(self) -> Dict:
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

    def __new__(cls, *args, **kwargs) -> Self:
        instance = super().__new__(cls)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance


class RhesultDict(dict):
    def __init__(self, connexion, *args, **kwargs) -> None:
        self._instruct, self._tablename = connexion.instruct

        for key, value in kwargs.items():
            self[key] = value

    def _to_json(self) -> str:
        return json.dumps(self)


class RhesultOne(Rhesult):

    def _to_json(self) -> str:
        return json.dumps(self._to_dict())

    def delete(self):
        self._instruct.delete(self._tablename, self.pk)

    def save(self):
        return self._connexion.update(self.pk, **self._to_dict())

    def update(self, **kwargs):
        return self._connexion.update(self.pk, **kwargs)

    @property
    def json(self):
        return self._to_json()


class RhesultDictOne(RhesultDict):

    def delete(self):
        self._instruct.delete(self._tablename, self.pk)

    def save(self):
        return self._connexion.update(self.pk, **self)

    def update(self, **kwargs):
        return self._connexion.update(self.pk, **kwargs)

    @property
    def json(self):
        return self._to_json()


class RhesultMany(list):
    def __init__(self, connexion, *args, **kwargs) -> None:
        self._instruct, self._tablename = connexion.instruct
        self._command = kwargs

        for item in args:
            self._validate(item)
            self.append(item)

    def _analysis(self, **kwargs) -> bool:
        special = (
            'lt', 'gt', 'in',
            'bet', 'nin', 'ne',
            'le', 'ge', 'max',
            'min', 'sum', 'avg',
            'reg', 'ireg', 'like'
        )
        if kwargs and len(kwargs) > 0:
            for key in kwargs.keys():
                if '::' in key:
                    keys = key.split('::')[1:]
                    for i in keys:
                        if i not in special:
                            return True
        return False

    def exclude(self, **kwargs) -> Self:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.exclude(self._tablename, **self._command)
            result = [RhesultOne(self, dict(item)) for item in result]
            return self.__class__(self._connexion, result)
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def sort(self, *args, **kwargs) -> Self:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.sort(
                self._tablename,
                *args,
                **self._command
            )
            result = [RhesultOne(self, dict(item)) for item in result]
            return self.__class__(self._connexion, result)
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def limit(self, n: int = 5, offset: int = 0) -> Self:
        result = self._instruct.limit(
            self._tablename,
            n,
            offset,
            **self._command
        )
        result = [RhesultOne(self, dict(item)) for item in result]
        return self.__class__(self._connexion, result)

    def count(self) -> int:
        return len(self)

    def exists(self) -> bool:
        return len(self) > 0

    def first(self) -> RhesultOne:
        return self[0]

    def last(self) -> RhesultOne:
        return self[-1]

    def filter(self, *args, **kwargs) -> Self:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.filter(
                self._tablename,
                *args,
                **self._command
            )
            result = [RhesultOne(self, dict(item)) for item in result]
            return self.__class__(self._connexion, result)
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def get(self, pk, **kwargs) -> RhesultOne | None:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.get(self._tablename, pk, **self._command)
            return RhesultOne(self, dict(result)) if result else None
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def _to_json(self) -> str:
        return json.dumps([item.to_dict() for item in self])

    def _validate(self, item):
        if not isinstance(item, RhesultOne):
            raise TypeError(f"Expected RhesultOne, got {type(item)}")

    def append(self, object: RhesultOne | None) -> None:
        self._validate(object)
        return super().append(object)

    def extend(self, iterable: Iterable[RhesultOne | None]) -> None:
        for item in iterable:
            self._validate(item)
        return super().extend(iterable)

    def insert(self, index: int, object: RhesultOne | None) -> None:
        self._validate(object)
        return super().insert(index, object)

    @property
    def json(self):
        return self._to_json()

    def __setitem__(self, index, object: RhesultOne | None) -> None:
        if isinstance(index, slice):
            for item in object:
                self._validate(item)
        else:
            self._validate(object)
        return super().__setitem__(index, object)

    def __iadd__(self, value: Iterable[RhesultOne | None]) -> Self:
        for item in value:
            self._validate(item)
        return super().__iadd__(value)


class RhesultDictMany(list):
    def __init__(self, connexion, *args, **kwargs) -> None:
        self._instruct, self._tablename = connexion.instruct
        self._command = kwargs

        for item in args:
            self._validate(item)
            self.append(item)

    def _analysis(self, **kwargs) -> bool:
        special = (
            'lt', 'gt', 'in',
            'bet', 'nin', 'ne',
            'le', 'ge', 'max',
            'min', 'sum', 'avg',
            'reg', 'ireg', 'like'
        )
        if kwargs and len(kwargs) > 0:
            for key in kwargs.keys():
                if '::' in key:
                    keys = key.split('::')[1:]
                    for i in keys:
                        if i not in special:
                            return True
        return False

    def exclude(self, **kwargs) -> Self:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.exclude(self._tablename, **self._command)
            result = [RhesultDictOne(self, item) for item in result]
            return self.__class__(self._connexion, result)
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def sort(self, *args, **kwargs) -> Self:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.sort(
                self._tablename,
                *args,
                **self._command
            )
            result = [RhesultDictOne(self, item) for item in result]
            return self.__class__(self._connexion, result)
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def limit(self, n: int = 5, offset: int = 0) -> Self:
        result = self._instruct.limit(
            self._tablename,
            n,
            offset,
            **self._command
        )
        result = [RhesultDictOne(self, item) for item in result]
        return self.__class__(self._connexion, result)

    def count(self) -> int:
        return len(self)

    def exists(self) -> bool:
        return len(self) > 0

    def first(self) -> RhesultDictOne:
        return self[0]

    def last(self) -> RhesultDictOne:
        return self[-1]

    def filter(self, *args, **kwargs) -> Self:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.filter(
                self._tablename,
                *args,
                **self._command
            )
            result = [RhesultDictOne(self, item) for item in result]
            return self.__class__(self._connexion, result)
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def get(self, pk, **kwargs) -> RhesultDictOne | None:
        if self._analysis(**kwargs):
            self._command.update(kwargs)
            result = self._instruct.get(self._tablename, pk, **self._command)
            return RhesultDictOne(self, result) if result else None
        else:
            # traiter en python car aucune autre table n'est concernée
            result = None
            return result

    def _to_json(self) -> str:
        return json.dumps([item for item in self])

    def _validate(self, item):
        if not isinstance(item, RhesultDictOne):
            raise TypeError(f"Expected RhesultDictOne, got {type(item)}")

    def append(self, object: RhesultDictOne | None) -> None:
        self._validate(object)
        return super().append(object)

    def extend(self, iterable: Iterable[RhesultDictOne | None]) -> None:
        for item in iterable:
            self._validate(item)
        return super().extend(iterable)

    def insert(self, index: int, object: RhesultDictOne | None) -> None:
        self._validate(object)
        return super().insert(index, object)

    @property
    def json(self):
        return self._to_json()

    def __setitem__(self, index, object: RhesultDictOne | None) -> None:
        if isinstance(index, slice):
            for item in object:
                self._validate(item)
        else:
            self._validate(object)
        return super().__setitem__(index, object)

    def __iadd__(self, value: Iterable[RhesultDictOne | None]) -> Self:
        for item in value:
            self._validate(item)
        return super().__iadd__(value)


class RhesultNone(Rhesult):
    def __init__(self, connexion) -> None:
        super().__init__(connexion)
        self._connexion = None


class RhesultDictNone(RhesultDict):
    def __init__(self, connexion) -> None:
        super().__init__(connexion)
        self._connexion = None

# RhesultNone = None
