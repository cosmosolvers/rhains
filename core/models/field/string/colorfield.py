from typing import Any, Callable

from ..field import Field

from exceptions.core.models import field

from utils.const import HEX_COLOR_PATTERN, HEX_COLOR_NAMES
from utils.color import (
    hex_to_rgb,
    rgb_to_hex,
    rgb_to_hsl,
    hsl_to_rgb,
    rgba_to_hsla,
    hsla_to_rgba
)


class HexadecimalColorField(Field):
    """
    HEXADECIMAL COLOR FIELD
    =======================
    champ de couleurs au format hexadécimal

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise HexadecimalColorFieldValueError: si la valeur n'est pas valide
    :raise HexadecimalColorFieldLengthError: si la valeur est trop longue

    :return: str
    """

    def __init__(
        self,
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None,
        choices: list[str] | None = None
    ):
        self._max_length = 8
        if default is not None and not HEX_COLOR_PATTERN.match(default):
            raise field.HexadecimalColorFieldValueError("Invalid default hex color value")

        self._choices = choices
        if choices:
            for choice in choices:
                if not HEX_COLOR_PATTERN.match(choice):
                    raise field.HexadecimalColorFieldValueError(
                        f"{choice} is not a valid hex color value")

            if default and default not in choices:
                raise field.HexadecimalColorFieldValueError(f"{default} is not in choices")

        if len(default) > self._max_length:
            raise field.HexadecimalColorFieldLengthError(f"{default} too long")

        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def to_rgb(self) -> tuple[int, int, int]:
        return hex_to_rgb(self._value)

    def to_hsl(self) -> tuple[int, int, int]:
        return rgb_to_hsl(*self.to_rgb())

    def rgb_to_hex(self, rgb: tuple[int, int, int]) -> str:
        return rgb_to_hex(*rgb)

    def hsl_to_rgb(self, hsl: tuple[int, int, int]) -> tuple[int, int, int]:
        return hsl_to_rgb(*hsl)

    def rgba_to_hsla(self, rgba: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return rgba_to_hsla(*rgba)

    def hsla_to_rgba(self, hsla: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
        return hsla_to_rgba(*hsla)

    def name_to_hex(self, name: str) -> str:
        return HEX_COLOR_NAMES.get(name, None)

    def _validated(self, value: Any) -> bool:
        if not isinstance(value, str) or not HEX_COLOR_PATTERN.match(value):
            raise field.HexadecimalColorFieldValueError(f"{value} is not a valid hex color value")
        return super()._validated(value)
