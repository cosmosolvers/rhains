from typing import Any, Optional
from datetime import datetime
import pytz

from ..field import Field

from exceptions.core.models import field


class DateTimeField(Field):
    """
    DATETIME FIELD
    ==============
    Field pour les dates et heures
    """

    def __init__(
        self,
        format: Optional[str] = '%Y-%m-%d %H:%M:%S',
        tz: Optional[str] = None,
        max_datetime: Optional[datetime | str] = None,
        min_datetime: Optional[datetime | str] = None,
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
        self._min_datetime = min_datetime
        if self._min_datetime:
            if not isinstance(self._min_datetime, str):
                try:
                    self._min_datetime = self._min_datetime.strftime(self._format)
                except Exception as e:
                    raise field.DateTimeFieldFormatError(e)
            self._min_datetime = self.__parse_datetime(self._min_datetime)

        self._max_datetime = max_datetime
        if self._max_datetime:
            if not isinstance(self._max_datetime, str):
                try:
                    self._max_datetime = self._max_datetime.strftime(self._format)
                except Exception as e:
                    raise field.DateTimeFieldFormatError(e)
            self._max_datetime = self.__parse_datetime(self._max_datetime)

        self._auto_updated = auto_updated
        self._auto_created = auto_created
        if self._auto_created:
            default = self.__parse_datetime(
                datetime.now().strftime(self._format)
            )

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
                value = value.strftime(self._format)
            except Exception as e:
                raise field.DateTimeFieldValidationError(e)
        value = self.__parse_datetime(value)
        self._validated(value)
        return super().__set__(instance, value)

    def _validated(self, value: Any) -> bool:
        if self._min_datetime and value < self._min_datetime:
            raise field.DateTimeFieldValidationError(
                f"Date cannot be earlier than {self._min_datetime}")
        if self._max_datetime and value > self._max_datetime:
            raise field.DateTimeFieldValidationError(
                f"Date cannot be later than {self._max_datetime}")
        return super()._validated(value)

    def __parse_datetime(self, value: str) -> datetime:
        try:
            dt = datetime.strptime(value, self._format)
            if self._tz:
                tz = pytz.timezone(self._tz)
                dt = tz.localize(dt)
            return dt
        except ValueError:
            raise field.DateTimeFieldValidationError(
                f"Datetime format should be one of {self._format}")

    def load(self, value: str) -> datetime:
        return self.__parse_datetime(value)

    def dump(self, value: datetime) -> str:
        return value.strftime(self._format)
