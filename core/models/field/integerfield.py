from typing import Any, List, Tuple, Optional

from .field import Field

from exception.core.models import field


class IntegerField(Field):
    """
    INTEGER FIELD
    ============
    ensemble des entiers naturels IN
    """

    def __init__(
            self,
            nullable: bool = True,
            default: Optional[int] = None,
            primary_key: bool = False,
            unique: bool = False,
            editable: bool = True,
            check: Optional[Any] = None,
            min: Optional[int] = None,
            max: Optional[int] = None,
            max_digits: Optional[int] = None,
            min_digits: Optional[int] = None,
            interval: Optional[List[int]] = None,
            choices: Optional[Tuple[int]] = None,
    ):
        super().__init__(nullable, default, primary_key, unique, editable, check)
        self.encapsule_type = 'INT'

        self._validated_default()
        self._validate_min(min)
        self._validate_max(max)
        self._validate_max_digits(max_digits)
        self._validate_min_digits(min_digits)
        self._validate_interval(interval)
        self._validate_choices(choices)

    def _validated_default(self):
        try:
            self._default = int(self._default) if self._default else None
        except ValueError:
            raise field.IntegerFieldDefaultError(f"{self._default} can't be loaded")

    def _validate_min(self, min: Optional[int]):
        self._min = min
        if min and not self._default:
            self._default = self._min

    def _validate_max(self, max: Optional[int]):
        if self._min and max:
            raise field.FieldOverUseError("max and min can't be defined together")

        self._max = max
        if max and not self.default:
            raise field.FieldDefaultError("default value is required")

    def _validate_max_digits(self, max_digits: Optional[int]):
        self._max_digits = max_digits
        if self._max_digits and not self.default:
            raise field.FieldDefaultError("default value is required")
        if self._max_digits and len(str(self.default)) > self._max_digits:
            raise field.FieldDefaultError(f"default value must have {self._max_digits} digits")

    def _validate_min_digits(self, min_digits: Optional[int]):
        self._min_digits = min_digits
        if self._min_digits and not self.default:
            raise field.FieldDefaultError("default value is required")
        if self._min_digits and len(str(self.default)) < self._min_digits:
            raise field.FieldDefaultError(f"default value must have {self._min_digits} digits")

    def _validate_interval(self, interval: Optional[List[int, int]]):
        if interval:
            if self._max or self.min:
                raise field.FieldOverUseError("if interval define can't be defined min or max")
            if len(interval) != 2:
                raise field.FieldIntervalError("interval value must have 2 values")
            if interval[0] > interval[-1]:
                raise field.FieldIntervalError("interval value must have 2 ascending values")
            self._interval = interval
            if not self._default:
                raise field.FieldDefaultError("default value is required")
            if self._default > self._interval[-1] or self._default < self._interval[0]:
                raise field.FieldDefaultError(
                    f"default value must be in [{self._interval[0]}, {self._interval[-1]}] interval"
                )

    def _validate_choices(self, choices: Optional[Tuple[int]]):
        if choices:
            for i in choices:
                if not isinstance(i, int):
                    raise field.IntegerFieldError(f"{i} must be int type")
            self._choices = choices
            if not self.default:
                self._default = self._choices[0]
            if self.default not in self._choices:
                raise field.FieldDefaultError(f"default value must be in {self._choices}")

    def load(self, value: Any) -> int:
        try:
            value = int(value)
            return int(value)
        except ValueError:
            raise field.IntegerFieldLoadError(f"{value} can't be loaded")

    def dump(self) -> int:
        try:
            value = int(value)
            return int(self._value)
        except ValueError:
            raise field.IntegerFieldDumpError(f"{value} can't be encapsuled")

    def validate(self, value: Any) -> bool:
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

    def item(self):
        self._item = super().item()
        if self._min:
            self._item += f" CHECK ({self._name} >= {self._min})"
        if self._max:
            self._item += f" CHECK ({self._name} <= {self._max})"
        if self._max_digits:
            self._item += f" CHECK (LENGTH({self._name}) <= {self._max_digits})"
        if self._min_digits:
            self._item += f" CHECK (LENGTH({self._name}) >= {self._min_digits})"
        if self._choices:
            self._item += f" CHECK ({self._name} IN {self._choices})"
        return self._item
