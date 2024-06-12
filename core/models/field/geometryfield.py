from typing import Any, Callable, Optional
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry
import json

from .field import Field

from exception.core.models import field


class GeometryField(Field):
    """
    GEOMETRY FIELD
    ==============
    Champ pour les objets géométriques

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise GeometryFieldValueError: si la valeur n'est pas valide
    :raise FieldUniqueError: si le champ est unique et nullable
    :raise FieldPrimarykeyError: si le champ est primaire et nullable
    :raise FieldDefaultError: si la valeur par defaut n'est pas valide
    :raise FieldCheckError: si la fonction de validation n'est pas valide
    :raise FieldNullableError: si la valeur est nulle et non autorisée
    :raise FieldEditableError: si la valeur est non editable

    :return: BaseGeometry
    """

    def __init__(
        self,
        nullable: bool = True,
        default: Optional[BaseGeometry] | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if default:
            if not self._validated_geometry(default):
                raise field.GeometryFieldError(f"{default} is not a valid geometry")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def _validated_geometry(self, value: Any) -> bool:
        if isinstance(value, BaseGeometry):
            return True

    def load(self, value: str) -> BaseGeometry:
        return shape(json.loads(value))

    def dump(self, value: BaseGeometry) -> str:
        return json.dumps(value.__geo_interface__)

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and self._validated_geometry(value)
