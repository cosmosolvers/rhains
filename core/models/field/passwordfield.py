from typing import Any, Callable, Optional
import bcrypt

from .field import Field

from exception.core.models import field


class PasswordField(Field):
    """
    PASSWORD FIELD
    ==============
    champ pour stocker des mots de passe

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise PasswordFieldError: si la valeur par defaut n'est pas valide
    :raise PasswordFieldError: si la valeur n'est pas un mot de passe

    :return: str
    """

    def __init__(
        self,
        nullable: bool = True,
        default: Optional[str] = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if default:
            if not self._validated_password(default):
                raise field.PasswordFieldError(f"{default} is not a valid password")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def hash_password(self, password: str) -> str:
        """hash password for storing in database"""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str, hashed: str) -> bool:
        """check password"""
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def __set__(self, instance, value):
        value = self.hash_password(value)
        return super().__set__(instance, value)

    def _validated_password(self, value: Any) -> bool:
        if isinstance(value, str) and len(value) > 0:
            return True
        return False

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and self._validated_password(value)
