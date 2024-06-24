"""
"""
from typing import Any, Optional, Callable

# exception class
from exception.core.models import field
from utils.validefunc import validate_function_ckeck, validate_function_default


class Field:
    """
    FIELD
    =====
    class de base pour les champs

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise FieldUniqueError: si le champ est unique et nullable
    :raise FieldPrimarykeyError: si le champ est primaire et nullable
    :raise FieldDefaultError: si la valeur par defaut n'est pas valide
    :raise FieldCheckError: si la fonction de validation n'est pas valide
    :raise FieldNullableError: si la valeur est nulle et non autorisée
    :raise FieldEditableError: si la valeur est non editable

    :return: None
    """

    def __init__(
            self,
            nullable: bool = True,
            # value par defaut | verifie si ce n'est pas une function a executer
            default: Optional[Any] = None,
            # lors de la creation de la table
            primary_key: bool = False,
            # lors de la creation de la table
            unique: bool = False,
            # lors de la modification de la table
            editable: bool = True,
            # validateur de donnée (definir une fonction de validation) ex: lambda x: x > 0
            check: Callable[..., Any] | None = None,
    ):
        self._value = None
        self._check = None
        self._nullable = nullable
        self._editable = editable
        self._unique = unique
        self.__validated_unique()

        self._primarykey = primary_key
        self.__validated_primarykey()

        if default:
            if not callable(default):
                self._value = default
            else:
                if not validate_function_default(default):
                    raise field.FieldDefaultError(f"{default} is not a valid function")
                self._value = default()
        self.__validated_default(default)

        if check:
            if not callable(check):
                raise field.FieldCheckError(f"{check} is not a valid function")
            else:
                if not validate_function_ckeck(check):
                    raise field.FieldCheckError(f"{check} is not a valid function")
                self._check = check

        self.__name = None

    def __validated_unique(self):
        if self._nullable and self._unique:
            raise field.FieldUniqueError("nullable field can't be unique")

    def __validated_primarykey(self):
        if self._primarykey:
            if self._nullable:
                raise field.FieldPrimarykeyError("nullable field can't be primary key")
            self._unique = True

    def __validated_default(self, default):
        if default:
            if self._check and not self._check(default):
                raise field.FieldDefaultError(f"{self._value} doesn't match the check")
        else:
            if not self._nullable:
                raise field.FieldDefaultError("default value is required")
            if self._unique is True:
                raise field.FieldDefaultError("default value is required")
            if self._primarykey:
                raise field.FieldDefaultError("default value is required")
            if not self._editable:
                raise field.FieldEditableError("default value is required")

    # convertir une valeur de la base de donnée en donnée python
    # apres la lecture dans la base de donnée
    @staticmethod
    def load(value: Any) -> Any:
        raise NotImplementedError

    # convertir une donnée python en valeur de la base de donnée
    # avant l'ecriture dans la base de donnée
    def dump(self) -> Any:
        raise NotImplementedError

    # valider une donnée avant l'ecriture dans la base de donnée
    def _validated(self, value: Any) -> bool:
        if value is None and not self._nullable:
            raise field.FieldNullableError(f"{self._value} can't be null")
        if self._check and not self._check(value):
            raise field.FieldCheckError(f"{self._value} is not valid")
        return True

    # le nom sur lequel est stocker le champ
    def __set_name__(self, owner, name):
        self.__name = name

    def __set__(self, instance, value):
        # si une value existe ne pas la modifier
        if instance.__dict__.get(self.__name) and not self._editable:
            raise field.FieldEditableError(f"{self._value} can't be modified")
        if self._validated(value):
            instance.__dict__[self.__name] = value
            self._value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.__name, self._value)
