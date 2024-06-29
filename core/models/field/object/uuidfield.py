from typing import Any, Optional
import uuid
from ..field import Field
from exceptions.core.models import field


class UUIDField(Field):
    """
    UUID FIELD
    ==========
    Field for storing UUIDs.
    """

    def __init__(
        self,
        nullable: bool = True,
        default: uuid.UUID | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Optional[callable] = None
    ):
        if default and not isinstance(default, uuid.UUID):
            raise field.UUIDFieldDefaultError(f"{default} is not a valid default value")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: str) -> uuid.UUID:
        return uuid.UUID(value)

    def dump(self) -> str:
        return str(self._value)

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and isinstance(value, uuid.UUID)
