from typing import Optional, List
from datetime import datetime

from .datetimefield import DateTimeField


class DateTimeOffSetField(DateTimeField):
    """
    DATETIME OFFSET FIELD
    =====================
    Field pour les dates et heures avec decalage
    """

    def __init__(
        self,
        format: Optional[List[str]] = ['%Y-%m-%d %H:%M:%S %z'],
        tz: Optional[str] = None,
        max_datetime: Optional[datetime] = None,
        min_datetime: Optional[datetime] = None,
        auto_updated: bool = False,
        auto_created: bool = False,
        nullable: bool = True,
        default: datetime | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
    ):
        super().__init__(
            format=format,
            tz=tz,
            max_datetime=max_datetime,
            min_datetime=min_datetime,
            auto_updated=auto_updated,
            auto_created=auto_created,
            nullable=nullable,
            default=default,
            primary_key=primary_key,
            unique=unique,
            editable=editable,
        )
