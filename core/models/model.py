"""
MODELS FOR DATABASE
===================

class Templates(Model):
    ...
"""
from typing import Any

from .field.field import Field

from exception.core.models import model as md


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        new_class._fields = {k: v for k, v in attrs.items() if isinstance(v, Field)}
        return new_class


class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for field_name, field_instance in self._fields.items():
            if field_name in kwargs:
                setattr(self, field_name, kwargs[field_name])
            else:
                setattr(self, field_name, field_instance._value)

    def __setattr__(self, key: str, value: Any) -> None:
        if key in self._fields:
            field = self._fields[key]
            field.__set__(self, value)
        else:
            raise md.ModelFieldAttributeError(f"{key} is not a valid field")

    def __getattr__(self, key: str) -> Any:
        if key in self._fields:
            field = self._fields[key]
            return field.__get__(self)
        raise md.ModelFieldAttributeError(f"{key} is not a valid field")

    def __to_dict(self):
        return {key: getattr(self, key) for key in self._fields}

    def __str__(self) -> str:
        data = self.__to_dict()
        for k, v in data.items():
            if hasattr(v, 'primary_key') and v.primary_key:
                return v

    class Meta:
        database = 'default'
        abstract = False
        sort = ''
