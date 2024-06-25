from typing import Any, Optional, Dict

from ..field import Field

from exception.core.models import field

from ...model import Model


class Reference(Field):
    """
    RELATION
    ========

    :param to: model reference
    :param on_delete: action on delete
    :param nullable: nullable value
    :param default: default value

    :raise RelationModelError: if to is not a Model
    :raise RelationModelError: if on_delete is not a valid on_delete
    :raise RelationModelError: if default is not a to

    :return: Model

    :ON_DELETE:
    -----------
    NOAFFECT - Do nothing: delete the object
    RECURSIVE - Recursive delete: delete all related objects
    PROTECT - Protect delete: raise an error if there are related objects
    """

    def __init__(
        self,
        to: Optional[Model] = None,
        # NOAFFECT - RECURSIVE - PROTECT
        on_delete: str = 'NOAFFECT',
        nullable: bool = True,
        default: Any = None,
        unique: bool = False,
    ):
        if not to:
            raise field.RelationModelError("to is required")
        if not isinstance(to, Model):
            raise field.RelationModelError(f"{to} is not a Model")
        if on_delete not in ['NOAFFECT', 'RECURSIVE', 'PROTECT']:
            raise field.RelationModelError(f"{on_delete} is not a valid on_delete")
        if default and not isinstance(default, to):
            raise field.RelationModelError(f"{default} is not a {to}")
        super().__init__(
            nullable=nullable,
            default=default,
            unique=unique
        )
        self._to = to
        self._on_delete = on_delete

    def load(self, value: Dict) -> Any:
        return self._to(value)

    def dump(self) -> Any:
        return str(self._value)

    def _validated(self, value: Any) -> bool:
        if not isinstance(value, self._to):
            raise field.RelationModelError(f"{value} is not a {self._to}")
        return super()._validated(value)
