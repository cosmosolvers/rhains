from typing import Any, Callable

from .field import Field

from exception.core.models import field


class PercentField(Field):
    """
    PERCENT FIELD
    =============
    champ de pourcentage
    """

    def __init__(
        self,
        nullable: bool = True,
        default: float | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        default = default if default and not callable(default) else default()
        if default and not isinstance(default, (int, float)):
            raise field.FieldDefaultError(f"{default} is not a valid default value")
        if default and not 0 <= default <= 100:
            raise field.FieldDefaultError(f"{default} is not a valid default value")

        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: float) -> float:
        return value

    def dump(self) -> float:
        return self._value

    def to_decimal(self) -> float:
        return self._value / 100

    def from_decimal(self, value: float) -> float:
        return value * 100

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and 0 <= value <= 100
