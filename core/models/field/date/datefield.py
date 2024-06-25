from typing import Any, Optional, List
from datetime import datetime
import pytz

from ..field import Field

from exception.core.models import field


class DateField(Field):
    """
    DATE FIELD
    ==========

    Field pour les dates
    """

    def __init__(
        self,
        format: Optional[List[str]] = ['%Y-%m-%d'],
        tz: Optional[str] = None,
        max_date: Optional[datetime] = None,
        min_date: Optional[datetime] = None,
        auto_updated: bool = False,
        auto_created: bool = False,
        nullable: bool = True,
        default: datetime | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
    ):
        self._format = format
        self._tz = tz
        self._min_date = min_date
        self._max_date = max_date
        self._auto_update = auto_updated
        self._auto_created = auto_created
        if self._auto_created:
            default = self.__parse_date(datetime.now().strftime(self._format[0]))

        super().__init__(
            nullable=nullable,
            default=default,
            primary_key=primary_key,
            unique=unique,
            editable=editable,
        )

    def __set__(self, instance, value):
        if not isinstance(value, str):
            try:
                value = value.strftime(self._format[0])
            except Exception as e:
                raise field.DateFieldValidationError(e)
        value = self.__parse_date(value)
        self._validated(value)
        return super().__set__(instance, value)

    def _validated(self, value: datetime) -> bool:
        if self._min_date and value < self._min_date:
            raise field.DateFieldValidationError(f"Date cannot be earlier than {self._min_date}")
        if self._max_date and value > self._max_date:
            raise field.DateFieldValidationError(f"Date cannot be later than {self._max_date}")
        return super()._validated(value)

    def __parse_date(self, value: str) -> datetime:
        for fmt in self._format:
            try:
                date = datetime.strptime(value, fmt)
                if self._tz:
                    tz = pytz.timezone(self._tz)
                    date = tz.localize(date)
                return date
            except ValueError:
                continue
        raise field.DateFieldValidationError(f"Date format should be one of {self._format}")

    def load(self, value: str) -> datetime:
        return self.__parse_date(value)

    def dump(self, value: datetime) -> Any:
        return value.strftime(self._format[0])
