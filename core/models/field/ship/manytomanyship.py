from .relationship import RelationShip
from ...model import Model

from typing import Any, List
import json

from exceptions.core.models import field


class ManyToManyShip(RelationShip):
    """
    ONE TO ONE SHIP
    ===============
    """

    def __init__(
        self,
        to: List[Model],
        relation_name: str
    ):
        super().__init__(
            to=to
        )
        self._relation_name = relation_name
        if not relation_name:
            self._relation_name = f"{self._to.__name__}_{self.__class__.__name__}"
        if isinstance(self._relation_name, str):
            raise field.ManyToManyShipError(f"{self._relation_name} is not a valid relation name")
        self._value = []
        self._on_delete = ''

    def load(self, value: Any) -> Any:
        return json.loads(value)

    def dump(self) -> Any:
        return json.dumps(self._value)

    def add(self, value: Any):
        if self._validated(value):
            value = str(value)
            if value not in self._value:
                self._value.append(value)

    def remove(self, value: Any):
        if self._validated(value):
            value = str(value)
            if value in self._value:
                self._value.remove(value)
