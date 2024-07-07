""""""
from typing import Any, Dict


class Attributes:
    def __init__(self, **kwargs) -> None:
        if not kwargs:
            raise ValueError(f'{kwargs} cannot be null')
        self.__attrs(kwargs)
        self.__name = None

    def __set_name__(self, owner, name):
        self.__name = name

    def __set__(self, instance, value: Dict):
        if not instance.__dict__.get(self.__name):
            raise AttributeError('invalid action')
        self.__attrs(value)

    def __attrs(self, value: Dict):
        for k, v in value.items():
            if isinstance(v, dict):
                attrs = Attributes(**v)
                setattr(self, k, attrs)
            else:
                setattr(self, k, v)

    def __getattr__(self, name: str) -> Any:
        return self.__dict__.get(name)
