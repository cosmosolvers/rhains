from .relationship import RelationShip
from core.models.model import Model

from typing import Any, List


class OneToOneShip(RelationShip):
    """
    ONE TO ONE SHIP
    ===============
    """

    def __init__(
        self,
        to: List[Model],
        nullable: bool = True,
        default: Any | None = None,
        on_delete: str = 'NOAFFECT'
    ):
        super().__init__(
            to, nullable,
            default,
            on_delete
        )
