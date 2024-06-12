from .reference import Reference

from typing import Any


class OneToOneField(Reference):
    """
    ONE TO ONE FIELD
    =================
    champ de relation un a un

    :param to: model reference
    :param on_delete: action on delete
    :param nullable: nullable value
    :param default: default value

    :raise RelationModelError: if to is not a Model
    :raise RelationModelError: if on_delete is not a valid on_delete
    :raise RelationModelError: if default is not a to

    :return: Model
    """

    def __init__(
        self,
        to,
        on_delete: str = 'NOAFFECT',
        nullable: bool = True,
        default: Any = None
    ):
        super().__init__(
            to=to,
            on_delete=on_delete,
            nullable=nullable,
            default=default,
            unique=True
        )
