from .reference import Reference

from typing import Any


class ForeignKey(Reference):
    """
    FOREIGN KEY
    ===========
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
            default=default
        )
