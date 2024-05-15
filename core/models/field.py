"""
"""
from typing import Any, List, Tuple, Optional, Union


# exception class
from rhains.exception.core.field import (
    FieldExceptionValueError,
    NullableExceptionError,
    FieldExceptionContainsError
)



class Field:
    """
    """

    def __init__(
            self,
            nullable: bool = False,
            default=None,
            primary_key: bool = False, # lors de la creation de la table
            unique: bool = False, # lors de la creation de la table
            editable: bool = True, # lors de la modification de la table
    ):
        self.nullable = nullable
        self.default = default
        self.primary_key = primary_key
        self.unique = unique
    
    # convertir une valeur de la base de donnée en donnée python apres la lecture dans la base de donnée
    def decapsule(self, value: Any) -> Any:
        raise NotImplementedError
    
    # convertir une donnée python en valeur de la base de donnée avant l'ecriture dans la base de donnée
    def encapsule(self, value: Any) -> Any:
        raise NotImplementedError
    
    # valider une donnée avant l'ecriture dans la base de donnée
    def validate(self, value: Any) -> bool:

        if not value and not self.nullable:
            raise NullableExceptionError(f"Value for {self.__class__.__name__.split('Field')[0].lower()} field cannot be null")
        
        return True
    
    # default value
    @property
    def default(self) -> Any:
        return self.default
    
    @default.setter
    def default(self, value: Any) -> None:
        self.default = value
    
    def __set__(self, instance, value):
        if not self.validate(value):
            raise FieldExceptionValueError(f"Invalid value for {self.__class__.__name__.split('Field')[0].lower()} field")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]



class IntegerField(Field):
    """
    INTEGERFIELD
    ============
    enseble des entiers relatifs IN
    """

    def __init__(
            self, 
            nullable: bool = False, 
            default=None,
            primary_key: bool = False, 
            unique: bool = False,
            editable: bool = True,
            min: int = None,
            max: int = None,
            choices: Optional[Tuple[int]] = None,
        ):
        super().__init__(nullable, default, primary_key, unique)

    def decapsule(self, value: Any) -> Any:
        return int(value)
    
    def encapsule(self, value: Any) -> Any:
        return int(value)
    
    def validate(self, value: Any) -> bool:

        if not isinstance(value, int):
            raise FieldExceptionValueError(f"Value for {self.__class__.__name__.split('Field')[0].lower()} field must be an integer")

        if self.min and value < self.min:
            raise FieldExceptionValueError(f"Value for {self.__class__.__name__.split('Field')[0].lower()} field must be greater than {self.min}")
        
        if self.max and value > self.max:
            raise FieldExceptionValueError(f"Value for {self.__class__.__name__.split('Field')[0].lower()} field must be less than {self.max}")
        
        if self.choices and value not in self.choices:
            raise FieldExceptionContainsError(f"Value for {self.__class__.__name__.split('Field')[0].lower()} field must be in {self.choices}")
        
        self.super().validate(value)
