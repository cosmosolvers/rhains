from .reference import Reference

from typing import Any
import json

from exception.core.models import field


class ManyToManyField(Reference):
    """
    MANY TO MANY FIELD
    ==================
    champ de relation un a plusieurs

    :param to: model reference
    :param relation_name: name of the relation

    :raise RelationModelError: if to is not a Model
    :raise RelationModelError: if on_delete is not a valid on_delete
    :raise RelationModelError: if relation_name is not a valid relation name

    :return: List
    """

    def __init__(
        self,
        to,
        relation_name: str = None,
    ):
        super().__init__(
            to=to
        )
        self._relation_name = relation_name
        if not relation_name:
            self._relation_name = f"{self._to.__name__}_{self.__class__.__name__}"
        if isinstance(self._relation_name, str):
            raise field.RelationModelError(f"{self._relation_name} is not a valid relation name")
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
