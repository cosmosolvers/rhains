from typing import Any, Callable, Optional, Dict, Tuple
import json

from .field import Field

from exception.core.models import field


class CallableField(Field):
    """
    CALLABLE FIELD
    ==============
    champ de functions
    """

    def __init__(
        self,
        nullable: bool = True,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        params: Optional[Dict[str, object]] = None
    ):
        super().__init__(
            nullable=nullable,
            primary_key=primary_key,
            unique=unique,
            editable=editable,
        )
        self._params = Tuple(params) if params else None

    def load(self, value: Any) -> Any:
        return json.loads(value)

    def dump(self) -> Any:
        return json.dumps(self._value)

    def _validated(self, value: Any) -> bool:
        if not self._wrap_function(value):
            raise field.CallableFieldError(f'{value} is not supported arguments')
        return super()._validated(value)

    def _wrap_function(self, func: Callable) -> Callable:
        def wrapper(**kwargs):
            if len(kwargs) != len(self._params):
                raise field.CallableFieldArgumentError(f"{kwargs} number of arguments invalid")
            for k, v in kwargs.items():
                if k not in self._params:
                    raise field.CallableFieldArgumentError(f"{k} is not argument")
                if not isinstance(v, self._params[k]):
                    raise field.CallableFieldArgumentTypeError(
                        f"{v} not is {self._params} instance")
            return self._value(**kwargs)
        return wrapper
