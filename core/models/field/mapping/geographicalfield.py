from typing import Any, Callable
import json
import geohash2

from ..field import Field

from exceptions.core.models import field


class GeographicalField(Field):
    """
    GEOGRAPHICAL FIELD
    ==================
    Champ pour les coordonnées géographiques (latitude, longitude)

    :param precision: precision de la valeur
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise GeographicalFieldValueError: si la valeur n'est pas valide
    :raise FieldUniqueError: si le champ est unique et nullable
    :raise FieldPrimarykeyError: si le champ est primaire et nullable
    :raise FieldDefaultError: si la valeur par defaut n'est pas valide
    :raise FieldCheckError: si la fonction de validation n'est pas valide
    :raise FieldNullableError: si la valeur est nulle et non autorisée
    :raise FieldEditableError: si la valeur est non editable

    :return: tuple[float, float]
    """

    def __init__(
        self,
        precision: int = 12,
        nullable: bool = True,
        default: tuple[float, float] | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if precision < 1 or precision > 12:
            raise field.GeographicalFieldValueError("Precision must be between 1 and 12")

        if default:
            if not self._validated_coordinates(default):
                raise field.GeographicalFieldError(f"{default} is not a valid coordinates")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )
        self._precision = precision

    def _validated_coordinates(self, value: Any) -> bool:
        return len(value) == 2 and -90 <= value[0] <= 90 and -180 <= value[1] <= 180

    def load(self, value: Any) -> Any:
        return json.loads(value)

    def dump(self, value: Any) -> str:
        return json.dumps(value)

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and self._validated_coordinates(value)

    def encode(self):
        return geohash2.encode(self._value[0], self._value[1], self._precision)

    def decode(self, value: str):
        return geohash2.decode(value)
