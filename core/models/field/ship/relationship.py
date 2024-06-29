from typing import List, Any

from ..field import Field

from exceptions.core.models import field
from ...model import Model


class RelationShip(Field):
    """
    RELATIONSHIP
    ============
    """

    def __init__(
        self,
        to: List[Model],
        nullable: bool = True,
        default: Any | None = None,
        on_delete: str = 'NOAFFECT',
    ):
        for model in to:
            if not issubclass(model, Model):
                raise field.RelationShipValueError("Invalid model")

        if on_delete not in ['NOAFFECT', 'RECURSIVE', 'PROTECT']:
            raise field.RelationModelError(f"{on_delete} is not a valid on_delete")

        if default and not isinstance(default, tuple(to)):
            raise field.RelationShipValueError("Default value must be a field instance")

        super().__init__(
            nullable=nullable,
            default=default,
        )
        self._to = to
        self._on_delete = on_delete

    def load(self, value: Any) -> Any:
        loading = value.split("_")
        if len(loading) != 2:
            raise field.RelationShipValueError("Invalid value")
        value, type_ = loading
        for model in self._to:
            if model.__name__ == type_:
                return model.get(value)

    def dump(self, value: Any) -> Any:
        return f"{str(value)}_{type(value).__name__}"

    def _validated(self, value: Any) -> bool:
        type_ = type(value)
        if type_ not in self._to:
            raise field.RelationShipValueError(f"{type_} is not a valid model")
        return super()._validated(value) and isinstance(value, self._to)
