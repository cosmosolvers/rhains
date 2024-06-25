from typing import Any, List, Tuple, Optional, Union
from decimal import Decimal, getcontext

from ..field import Field

from exception.core.models import field


class DecimalField(Field):
    """
    DECIMAL FIELD
    =============
    ensemles des nombres decimaux ID
    """

    def __init__(
        self,
        nullable: bool = True,
        default: Optional[float | int | str] = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Optional[Any] = None,
        min: Optional[float | str | int] = None,
        max: Optional[float | str | int] = None,
        max_digits: Optional[int] = None,
        min_digits: Optional[int] = None,
        decimal_places: Optional[int] = None,
        interval: Optional[List[float | str | int]] = None,
        choices: Optional[Tuple[float | str | int]] = None
    ):
        default = default if not callable(default) else default()
        default = Decimal(default) if default else None
        super().__init__(nullable, default, primary_key, unique, editable, check)

        self._validate_min(min)
        self._validate_max(max)
        self._validate_max_digits(max_digits)
        self._validate_min_digits(min_digits)
        self._validate_decimal_places(decimal_places)
        self._validate_interval(interval)
        self._validate_choices(choices)

        self.encapsule_type = f'DECIMAL({self._max_digits}, {self._decimal_places})'
        getcontext().prec = self._max_digits
        self.scale = 1 / self._decimal_palces * 10
        self._value = self._value.quantize(Decimal(self.scale))

    def _validate_min(self, min: Optional[float | str | int]):
        self._min = Decimal(min)
        if min and not self._value:
            self._value = self._min

    def _validate_max(self, max: Optional[float | str | int]):
        if self._min and max:
            raise field.FieldOverUseError("max and min can't be defined together")

        if max and not self._value:
            raise field.FieldDefaultError("default value is required")
        self._max = Decimal(max)

    def _validate_max_digits(self, max_digits: Optional[int]):
        if not max_digits:
            raise field.DecimalFieldError("max_digits value is required")
        self._max_digits = max_digits
        if not self._value:
            raise field.FieldDefaultError("default value is required")
        if self._max_digits and len(str(self._value)) > self._max_digits:
            raise field.FieldDefaultError(f"default value must have {self._max_digits} digits")

    def _validate_min_digits(self, min_digits: Optional[int]):
        self._min_digits = min_digits
        if self._min_digits and not self._value:
            raise field.FieldDefaultError("default value is required")
        if self._min_digits and len(str(self._value)) < self._min_digits:
            raise field.FieldDefaultError(f"default value must have {self._min_digits} digits")

    def _validate_decimal_places(self, decimal_places: Optional[int]):
        if not decimal_places:
            raise field.DeciamlFieldError("decimal_places value is required")
        self._decimal_palces = decimal_places

    def _validate_interval(self, interval: Optional[List[float | str | int]]):
        if interval:
            if self._max or self.min:
                raise field.FieldOverUseError("if interval define can't be defined min or max")
            if len(interval) != 2:
                raise field.FieldIntervalError("interval value must have 2 value")
            if interval[0] > interval[-1]:
                raise field.FieldIntervalError("interval value must have 2 value ascendant")
            self._interval = [Decimal(interval[0]), Decimal(interval[-1])]

            if self._interval and not self._value:
                raise field.FieldDefaultError("default value is required")
            if self._interval and (
                self._value > self._interval[-1] or self._value < self._interval[0]
            ):
                raise field.FieldDefaultError(
                    f"default value must in [{self._interval[0]}, {self._interval[-1]}] interval"
                )

    def _validate_choices(self, choices: Optional[Tuple[float | str | int]]):
        self._choices = (Decimal(i) for i in choices)
        if self._choices and not self._value:
            self._value = self._choices[0]
        if self._choices and self._value not in self._choices:
            raise field.FieldDefaultError(f"default value must be in {self._choices}")

    def load(self, value: Any) -> Any:
        try:
            value = Decimal(value).quantize(Decimal(self.scale))
            return value
        except ValueError:
            raise field.DecimalFieldLoadError(f"{value} can't be loaded")

    def dump(self) -> Any:
        try:
            return Decimal(self._value).quantize(Decimal(self.scale))
        except ValueError:
            raise field.DecimalFieldDumpError(f"{self._value} can't be encapsuled")

    def validate(self, value: Union[float, int, str]) -> bool:
        if self._min and value < self._min:
            raise field.FieldMinError(f"{value} must be greater than {self._min}")

        if self._max and value > self._max:
            raise field.FieldMaxError(f"{value} must be less than {self._max}")

        if self._max_digits and len(str(value)) > self._max_digits:
            raise field.FieldMaxDigitsError(f"{value} must have {self._max_digits} digits")

        if self._min_digits and len(str(value)) < self._min_digits:
            raise field.FieldMinDigitsError(f"{value} must have {self._min_digits} digits")

        if self._interval and (value > self._interval[-1] or value < self._interval[0]):
            raise field.FieldDefaultError(
                f"default value must in [{self._interval[0]}, {self._interval[-1]}] interval"
            )

        if self._choices and value not in self._choices:
            raise field.FieldChoicesError(f"{value} must be in {self._choices}")

        return super()._validated(value)
