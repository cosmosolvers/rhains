"""
"""
from typing import Any, Optional, Callable

# exception class
from exception.core.models import field


class Field:
    """
    FIELD
    =====
    class de base pour les champs
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
        self._nullable = nullable
        self._unique = unique
        self._editable = editable
        self._primarykey = primary_key
        self._default = default if not callable(default) else self.default()
        self._check = check

        self.__validated_unique()
        self.__validated_primarykey()
        self.__validated_check()
        self.__validated_default()

        self._value = self._default
        self.__name = None

    def __validated_unique(self):
        if self._nullable and self._unique:
            raise field.FieldUniqueError("nullable field can't be unique")

    def __validated_primarykey(self):
        if self._nullable and self._primarykey:
            raise field.FieldPrimarykeyError("nullable field can't be primary key")
        self._unique = True

    def __validated_check(self):
        if not self._wrap_function(self._check):
            raise field.FieldCheckError(f"{self._check} is not a valid function")

    def _wrap_function(self, check: Callable) -> Callable:
        def wrapper():
            return check(self._value)
        return wrapper

    def __validated_default(self):
        if self._default:
            if not self._check(self._default):
                raise field.FieldDefaultError(f"{self._default} doesn't match the check")
        else:
            if not self._nullable:
                raise field.FieldDefaultError("default value is required")
            if self._unique:
                raise field.FieldDefaultError("default value is required")
            if self._primary_key:
                raise field.FieldDefaultError("default value is required")

    # convertir une valeur de la base de donnée en donnée python
    # apres la lecture dans la base de donnée
    def load(self, value: Any) -> Any:
        raise NotImplementedError

    # convertir une donnée python en valeur de la base de donnée
    # avant l'ecriture dans la base de donnée
    def dump(self) -> Any:
        raise NotImplementedError

    # valider une donnée avant l'ecriture dans la base de donnée
    def _validated(self, value: Any) -> bool:
        if value is None and not self._nullable:
            raise field.FieldNullableError(f"{self.__name} can't be null")
        if self._check and not self._check(value):
            raise field.FieldCheckError(f"{self.__name} is not valid")
        return True

    # le nom sur lequel est stocker le champ
    def __set_name__(self, owner, name):
        self.__name = name

    def __set__(self, instance, value):
        # si une value existe ne pas la modifier
        if instance.__dict__.get(self.__name) and not self._editable:
            raise field.FieldEditableError(f"{self.__name} can't be modified")
        if self._validated(value):
            instance.__dict__[self.__name] = value
            self._value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.__name, self._default)


# class Field:

#     value = None

#     def __init__(
#         auto_updated: bool=False, # definit comme etant mis a jour automatiquement
#         auto_incr: bool=False, # definit comme etant incrementer automatiquement
#         choices: Tuple=None, # definit une liste de choix possibles *
#         max_length: int=None, # definit une longueur maximale
#         min_length: int=None, # definit une longueur minimale
#         power_of_ten: int=None, # definit la puissance de 10
#         on_delete: str=None, # definit une action a effectuer lors de la suppression
#         on_update: str=None, # definit une action a effectuer lors de la mise a jour
#     ):
#         pass
