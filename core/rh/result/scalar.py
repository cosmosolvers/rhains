""""""
from typing import Any
import json

from exception.core.rh.database import rhesult as rhs


class Scalar:
    def __init__(self, instance, collection) -> None:
        self.__instance = instance
        self.__collection = collection
        for k, v in self.__to_dict().items():
            setattr(self, k, v)

    def __setattr__(self, name: str, value: Any) -> None:
        self.__instance.__setattr__(name, value)

    def __getattr__(self, name: str):
        return self.__instance.__getattr__(name)

    def __to_dict(self):
        return self.__instance.__to_dict()

    def serializer(self):
        return json(self.__to_dict())

    def save(self):
        data = self.__to_dict()
        pk_field, pk_value = (
            (k, v)
            for k, v in data.items()
            if self._fields[k]._primarykey
        )
        del data[pk_field]
        data = {
            pk_field: pk_value,
            '$commit': data
        }
        self.__collection.update(**data)

    def delete(self):
        field, value = (
            (k, v)
            for k, v in self.__to_dict().items()
            if self._fields[k]._primarykey
        )
        self.__collection.delete({field: value})


class Matrix:
    def __init__(self, collection, *args):
        self.__collection = collection
        self.__models = []

        for model in args:
            self.__validate(model)
            self.__models.append(model)

    def __len__(self):
        return len(self.__models)

    def exists(self):
        return True if len(self.__models) > 0 else False

    def first(self):
        return self.__models[0]

    def last(self):
        return self.__models[-1]

    def sort(self, key: str, reverse: bool = False):
        self.__models.sort(key=lambda x: getattr(x, key), reverse=reverse)
        return self

    def limit(self, limit: int, offset: int = 0):
        return self.__models[offset:limit]

    def filter(self, **kwargs):
        return self.__class__(
            model
            for model in self.__models
            if all(
                getattr(model, key) == value
                for key, value in kwargs.items()
            )
        )

    def exclude(self, **kwargs):
        return self.__class__(
            model
            for model in self.__models
            if all(
                getattr(model, key) != value
                for key, value in kwargs.items()
            )
        )

    def insert(self, index: int, model):
        self.__validate(model)
        self.__models.insert(index, model)

    def append(self, model):
        self.__validate(model)
        self.__models.append(model)

    def extend(self, iterable):
        for model in iterable:
            self.__validate(model)
        self.__models.extend(iterable)

    def get(self, **kwargs):
        return self.filter(**kwargs).first()

    def update(self, **kwargs):
        witness = self.first()
        k, v = (
            (k, v)
            for k, v in witness.__to_dict().items()
            for item in self
            if item.__to_dict()[k] == v
        )
        if k is None or v is None:
            return None
        data = {
            k: v,
            '$commit': kwargs
        }
        return self.__collection.update(data)

    def delete(self):
        witness = self.first()
        k, v = (
            (k, v)
            for k, v in witness.__to_dict().items()
            for item in self
            if item.__to_dict()[k] == v
        )
        self.__collection.delete({k: v})

    def __validate(self, model):
        if not isinstance(model, Scalar):
            raise rhs.ModelViewListError("model is not a valid Model")
