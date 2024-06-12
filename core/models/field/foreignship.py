from .relationship import RelationShip
from ..model import Model

from typing import Any, List


class ForeignShip(RelationShip):
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
