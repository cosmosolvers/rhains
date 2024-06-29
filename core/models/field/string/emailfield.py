from typing import Any, Optional, Callable

from ..field import Field

from exceptions.core.models import field
from utils.const import EMAIL_REGEXP


class EmailField(Field):
    """
    EMAIL FIELD
    ===========
    champ d'email

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary key: cle primaire
    :param unique: valuer unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise EmailFieldValidationError: si la valeur n'est pas conforme a un email

    :return: str
    """

    def __init__(
            self,
            nullable: bool = True,
            default: Optional[str] = None,
            primary_key: bool = False,
            unique: bool = False,
            editable: bool = True,
            check: Optional[Callable] = None,
    ):
        super().__init__(
            nullable=nullable,
            default=default,
            primary_key=primary_key,
            unique=unique,
            editable=editable,
            check=check
        )
        if default and not EMAIL_REGEXP.match(default):
            raise field.EmailFieldValidationError(f"{default} is not valid email")

    def load(self, value: Any) -> Any:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        if not EMAIL_REGEXP.match(value):
            raise field.EmailFieldValidationError(f"{value} is not valid email")
        return super()._validated(value) and isinstance(value, str)
