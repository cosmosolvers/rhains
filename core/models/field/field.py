"""
"""
from typing import Any, Optional

# import inspect


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
            check: Optional[Any] = None,
    ):
        self._nullable = nullable
        # verifier que le si check est defini il est une fonction
        if check and not callable(check):
            raise field.FieldCheckError(f"{check} is not callable")
        self._check = check
        # verifier que la valeur par defaut exist si le champ n'est pas nullable
        if not nullable and not default:
            raise field.FieldDefaultError("default value is required")
        self._default = default if not callable(default) else self.default()
        # verifier que la valeur par defaut est valide
        if not self._validated(self._default):
            raise field.FieldDefaultError(f"{self._default} doesn't match the check")

        self._primary_key = primary_key
        self._unique = unique
        # verifier que le champ n'est pas nullable et primary_key
        if nullable and primary_key:
            raise field.FieldNullableError("nullable field can't be primary key")
        # verifier que le champ n'est pas nullable et unique
        if nullable and unique:
            raise field.FieldNullableError("nullable field can't be unique")

        self._editable = editable
        self._item: str = ''
        self.encapsule_type = None
        self._name = self._default

    # convertir une valeur de la base de donnée en donnée python
    # apres la lecture dans la base de donnée
    def load(self, value: Any) -> Any:
        raise NotImplementedError

    # convertir une donnée python en valeur de la base de donnée
    # avant l'ecriture dans la base de donnée
    def dump(self, value: Any) -> Any:
        raise NotImplementedError

    # valider une donnée avant l'ecriture dans la base de donnée
    def _validated(self, value: Any) -> bool:
        if not value and not self._nullable:
            raise field.FieldNullableError("{value} can't be empty")
        if self._check and not self._check(value):
            raise field.FieldCheckError(f"{value} doesn't match the check")
        return True

    def __set_name__(self, owner, name):
        self._name = name

    def __set__(self, instance, value):
        value = self.load(value)
        # si une value existe ne pas la modifier
        if instance.__dict__.get(self._name) and not self._editable:
            raise field.FieldEditableError(f"{self._name} can't be modified")
        if self._validated(value):
            instance.__dict__[self._name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name, self._default)

    def item(self):
        self._item = self.encapsule_type
        if self._nullable:
            self._item += ' NULL'
        else:
            self._item += ' NOT NULL'
        if self._default:
            self._item += f" DEFAULT {self._default}"
        if self._primary_key:
            self._item += ' PRIMARY KEY'
        if self._unique:
            self._item += ' UNIQUE'
        return self._item




class Field:
    
    value = None
    
    def __init__(
        auto_updated: bool=False, # definit comme etant mis a jour automatiquement
        auto_incr: bool=False, # definit comme etant incrementer automatiquement
        choices: Tuple=None, # definit une liste de choix possibles *
        max_length: int=None, # definit une longueur maximale
        min_length: int=None, # definit une longueur minimale
        power_of_ten: int=None, # definit la puissance de 10
        on_delete: str=None, # definit une action a effectuer lors de la suppression
        on_update: str=None, # definit une action a effectuer lors de la mise a jour
    ):
        pass
