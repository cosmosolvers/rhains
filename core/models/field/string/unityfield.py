from typing import Any, Callable, Optional, List, Dict

from ..field import Field

from exceptions.core.models import field


class ExchangeField(Field):
    """
    CURRENCY FIELD
    ==============

    champ de currency

    :param convert: list des autres unité et leur function de conversion vers celui -ci
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise ExchangeConvertError: si la fonction de conversion n'est pas valide

    :return: str
    """

    def __init__(
        self,
        # list des autres currency et leur function de conversion vers celui -ci
        convert: Optional[List[Dict[str, Callable]]] = None,
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )
        for i in convert:
            k, v = i.popitem()
            if not callable(v) or not self._validate_function_two_args(v):
                raise field.ExchangeConvertError(f"{v} is not a valid function")
            setattr(self, k, self._wrap_function(v))

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _wrap_function(self, check: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args):
            return check(*args)
        return wrapper
