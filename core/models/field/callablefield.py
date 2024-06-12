from typing import Any, Callable, Optional, List
import json

from .field import Field

from exception.core.models import field


class CallableField(Field):
    """
    CALLABLE FIELD
    ==============
    champ de functions

    :param nullable: valeur nulle autorisée
    :param unique: valeur unique
    :param default: valeur par defaut
    :param editable: valeur editable
    :param choices: liste des fonctions

    :raise CallableFieldValidationError: si la valeur n'est pas valide

    :return: callable
    """

    def __init__(
        self,
        nullable: bool = True,
        unique: bool = False,
        default: Optional[Callable[..., Any]] = None,
        editable: bool = True,
        choices: Optional[List[Callable]] = None
    ):
        if not isinstance(default, Callable):
            raise field.CallableFieldValidationError(f"{default} is not a valid function")

        self._choices = choices
        if choices:
            for choice in choices:
                if not callable(choice):
                    raise field.CallableFieldValidationError(f"{choice} is not a valid function")

            if default and not default not in choices:
                raise field.CallableFieldValidationError(f"{default} is not in choices")

        super().__init__(
            nullable=nullable,
            unique=unique,
            editable=editable,
        )

    def load(self, value: Any) -> Any:
        return json.loads(value)

    def dump(self) -> Any:
        return json.dumps(self._value)

    def _validated(self, value: Any) -> bool:
        if self._choices and value not in self._choices:
            raise field.CallableFieldValidationError(f"{value} is not in choices")

        if not callable(value):
            raise field.CallableFieldValidationError(f"{value} is not a valid function")
        return super()._validated(value)

    def __call__(self, *args, **kwargs):
        func = self._value
        if func is None:
            raise field.CallableFieldValidationError("No callable set")
        return func(*args, **kwargs)
