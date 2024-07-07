from typing import Optional
import re
from ..field import Field
from exceptions.core.models import field


class URLField(Field):
    """
    URL FIELD
    =========
    champ de lien url

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise URLFieldDefaultError: si la valeur par defaut n'est pas valide
    :raise URLFieldCheckError: si la fonction de validation n'est pas valide

    :return: str
    """

    def __init__(
        self,
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Optional[callable] = None
    ):
        if default and not self._validated_url(default):
            raise field.URLFieldDefaultError(f"{default} is not a valid default value")
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

    def dump(self, value) -> str:
        return value

    def _validated_url(self, value: str) -> bool:
        regex = re.compile(
            # http:// or https://
            r'^(?:http|ftp)s?://'
            # domaine
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            # localhost
            r'localhost|'
            # IP
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            # IPv6
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
            # port
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE
        )
        return re.match(regex, value) is not None

    def _validated(self, value: str) -> bool:
        return super()._validated(value) and self._validated_url(value)
