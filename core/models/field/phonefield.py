from typing import Optional, Any, Callable
import phonenumbers
from phonenumbers import NumberParseException, geocoder, carrier, timezone
from .field import Field
from exception.core.models import field


class PhoneField(Field):
    """
    PHONE FIELD
    ===========
    Champ pour les numéros de téléphone
    """

    def __init__(
        self,
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Optional[Callable[..., Any]] = None
    ):
        default = default if default and not callable(default) else default()
        if default and not isinstance(default, str):
            raise field.FieldDefaultError(f"{default} is not a valid default value")
        if default and not self._validate_phone(default):
            raise field.FieldDefaultError(f"{default} is not a valid default value")

        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def _validate_phone(self, value: str) -> bool:
        if not isinstance(value, str):
            raise field.PhoneFormatError(f"{value} is not a valid phone number")
        try:
            value = phonenumbers.parse(value, None)
            return phonenumbers.is_valid_number(value)
        except NumberParseException:
            raise field.PhoneFormatError(f"{value} is not a valid phone number")

    def load(self, value: str) -> str:
        if not self._validate_phone(value):
            raise field.PhoneFormatError(f"{value} is not a valid phone number")
        return self.format(value)

    def format(self, value: str) -> str:
        value = phonenumbers.parse(value, None)
        return phonenumbers.format_number(
            value,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )

    def dump(self) -> str:
        return self._value

    def get_country(self) -> str:
        try:
            return geocoder.description_for_number(
                phonenumbers.parse(self._value, None),
                "en"
            )
        except NumberParseException:
            raise field.PhoneFormatError(f"{self._value} is not a valid phone number")

    def get_region(self) -> str:
        try:
            parsed = phonenumbers.parse(self._value, None)
            return phonenumbers.region_code_for_number(parsed)
        except NumberParseException:
            raise field.PhoneFormatError(f"{self._value} is not a valid phone number")

    def get_number_type(self) -> str:
        try:
            parsed = phonenumbers.parse(self._value, None)
            phonetype = phonenumbers.number_type(parsed)
            return phonenumbers.PhoneNumberType(phonetype).name
        except NumberParseException:
            raise field.PhoneFormatError(f"{self._value} is not a valid phone number")

    def get_carrier(self) -> str:
        try:
            return carrier.name_for_number(
                phonenumbers.parse(self._value, None),
                "en"
            )
        except NumberParseException:
            raise field.PhoneFormatError(f"{self._value} is not a valid phone number")

    def get_timezone(self) -> str:
        try:
            return timezone.time_zones_for_number(
                phonenumbers.parse(self._value, None)
            )
        except NumberParseException:
            raise field.PhoneFormatError(f"{self._value} is not a valid phone number")

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and self._validate_phone(value)
