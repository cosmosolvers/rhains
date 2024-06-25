from typing import Any, Callable, Optional

from ..field import Field

from exception.core.models import field


class CounterField(Field):
    """
    COUNTER FIELD
    =============
    champ de compteur

    :param initial: valeur initiale
    :param max_counter: valeur maximale du compteur
    :param auto_reset: auto reset le compteur a la valeur initial
    :param incr: fonction d'incrementation
    :param auto_update: auto update la valeur
    :param nullable: valeur nulle autorisée
    :param check: fonction de validation

    :raise CounterFieldValidationError: si la valeur n'est pas valide
    :raise CounterFieldFunctionError: si la fonction n'est pas valide

    :return: int
    """

    def __init__(
        self,
        initial: Optional[int] = 0,
        # valeur maximale du compteur
        max_counter: Optional[int] = None,
        # auto reset le compteur a la valeur initial
        auto_reset: Optional[bool] = False,
        # fonction d'incrementation
        incr: Optional[Callable] = None,
        auto_updated: Optional[bool] = False,
        nullable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        super().__init__(
            nullable=nullable,
            default=initial,
            check=check
        )
        if incr is None:
            raise field.CounterFieldValidationError("No increment function set")
        if not callable(incr) or self._validate_function_ckeck(incr):
            raise field.CounterFieldValidationError(f"{incr} is not a valid function")

        self._incr = incr
        self._auto_updated = auto_updated
        self._max_counter = max_counter
        self._auto_reset = auto_reset

    def load(self, value: Any) -> Any:
        return value

    def dump(self) -> Any:
        return self._value

    def _validated(self, value: Any) -> bool:
        if not isinstance(value, int):
            raise field.CounterFieldValueError(f"{value} is not a valid value")
        return super()._validated(value)
