from typing import Any, Optional, Callable
from datetime import datetime, time

from ..field import Field

from exceptions.core.models import field


class TimeField(Field):
    """
    TIME FIELD
    ==========
    champ de temps

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise TimeFieldDefaultError: si la valeur par defaut n'est pas valide

    :return: time
    """

    def __init__(
        self,
        format: Optional[str] = '%H:%M:%S',
        max_time: Optional[time | str] = None,
        min_time: Optional[time | str] = None,
        auto_updated: bool = False,
        auto_created: bool = False,
        nullable: bool = True,
        default: datetime | str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        self._format = format
        self._min_time = min_time
        if self._min_time:
            if not isinstance(self._min_time, str):
                try:
                    self._min_time = self._min_time.strftime(self._format)
                except Exception as e:
                    raise field.TimeFieldFormatError(e)
            self._min_time = self.__parse_time(self._min_time)

        self._max_time = max_time
        if self._max_time:
            if not isinstance(self._max_time, str):
                try:
                    self._max_time = self._max_time.strftime(self._format)
                except Exception as e:
                    raise field.TimeFieldFormatError(e)
            self._max_time = self.__parse_time(self._max_time)

        self._auto_updated = auto_updated
        self._auto_created = auto_created
        if self._auto_created:
            default = self.__parse_time(
                datetime.now()
            )

        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def __set__(self, instance, value):
        if not isinstance(value, str):
            try:
                value = value.strftime(self._format)
            except Exception as e:
                raise field.TimeFieldValidationError(e)
        value = self.__parse_time(value)
        self._validated(value)
        return super().__set__(instance, value)

    def _validated(self, value: Any):
        if self._min_time and value < self._min_time:
            raise field.TimeFieldValidationError(f"Time cannot be earlier than {self._min_time}")
        if self._max_time and value > self._max_time:
            raise field.TimeFieldValidationError(f"time connt be later than {self._max_time}")
        return super()._validated(value)

    def __parse_time(self, value: str) -> time:
        try:
            dt = datetime.strptime(value, self._format)
            return time(dt.hour, dt.minute, dt.second)
        except Exception as e:
            raise field.TimeFieldParseError(e)

    def load(self, value: str) -> datetime:
        return self.__parse_time(value)

    def dump(self, value: datetime) -> str:
        return value.strftime(self._format)
