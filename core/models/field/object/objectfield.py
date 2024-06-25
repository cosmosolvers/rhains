from typing import Any, Callable, Optional
import json

from ..field import Field

from exception.core.models import field


class ObjectField(Field):
    """
    OBJECT FIELD
    ============
    champ pour stocker des objets

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise FieldDefaultError: si la valeur par defaut n'est pas valide
    :ObjectFieldError: si la valeur n'est pas un objet

    :return: object
    """

    def __init__(
        self,
        nullable: bool = True,
        default: Optional[object] = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if default:
            if not self._validated_object(default):
                raise field.ObjectFieldError(f"{default} is not a valid object")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def _validated_object(self, value: Any) -> bool:
        if isinstance(value, object):
            return True
        return False

    def load(self, value: str) -> dict[str, Any]:
        return json.loads(value)

    def dump(self) -> str:
        return json.dumps(self._value)

    def _validated(self, value: Any) -> bool:
        return self._validated_object(value) and super()._validated(value)
