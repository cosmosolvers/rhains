from typing import Any, Callable, Optional
import json
import networkx as nx
from networkx.readwrite import json_graph

from .field import Field

from exception.core.models import field


class GraphField(Field):
    """
    GRAPH FIELD
    ===========
    Champ pour les objets graphiques (graphes)

    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise GraphFieldError: si la valeur par defaut n'est pas un graphe valide

    :return: networkx.Graph
    """

    def __init__(
        self,
        nullable: bool = True,
        default: Optional[nx.Graph] | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if default:
            if not self._validated_graph(default):
                raise field.GraphFieldError(f"{default} is not a valid graph")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def _validated_graph(self, value: Any) -> bool:
        if isinstance(value, nx.Graph):
            return True

    def load(self, value: str) -> nx.Graph:
        return json_graph.node_link_graph(json.loads(value))

    def dump(self) -> str:
        return json.dumps(json_graph.node_link_data(self))

    def _validated(self, value: Any) -> bool:
        return super()._validated(value) and self._validated_graph(value)
