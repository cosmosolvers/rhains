from typing import Any, Callable, Tuple
import json
import geohash2

from ..field import Field

from exceptions.core.models import field


class GPS:
    def __init__(self, latitude: float, longitude: float, precision: int = 12):
        self.latitude = latitude
        self.longitude = longitude
        self.precision = precision

    def __eq__(self, value: object) -> bool:
        return isinstance(value, GPS) and value.lat == self.lat and value.lng == self.lng

    @property
    def lng(self):
        return self.longitude

    @property
    def lat(self):
        return self.latitude

    @property
    def encode(self):
        return geohash2.encode(self.latitude, self.longitude, self.precision)

    def decode(self, value: str):
        return geohash2.decode(value)


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
        default: Tuple[float, float] | None = None,
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

    def load(self, value: str) -> GPS:
        return GPS(*tuple(json.loads(value)), self._precision)

    def dump(self, value: Tuple) -> str:
        return json.dumps(value)

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and self._validated_coordinates(value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return GPS(*super().__get__(instance, owner), self._precision)
