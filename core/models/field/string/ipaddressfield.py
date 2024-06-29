from typing import Any, Callable
import ipaddress

from ..field import Field

from exceptions.core.models import field


class IPAddressField(Field):
    """
    IP ADDRESS FIELD
    ================
    Champ pour les adresses IP (IPv4 ou IPv6)

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise IPAddressFieldError: si la valeur par defaut n'est pas une adresse ip valide

    :return: ipaddress.IPv4Address | ipaddress.IPv6Address
    """

    def __init__(
        self,
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if default and not self._validate_ip_address(default):
            raise field.IPAddressFieldError(f"{default} is not a valid ip address")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def _validate_ip_address(self, value: str) -> bool:
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

    def load(self, value: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
        return ipaddress.ip_address(value)

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and self._validate_ip_address(value)
