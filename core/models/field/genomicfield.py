from typing import Any, Callable

from .field import Field

from exception.core.models import field


class GenomicField(Field):
    """
    GENOMIC FIELD
    =============
    Champ pour les séquences génomiques (ADN, ARN, protéines)

    :param sequence: type de séquence (ADN, ARN, protéines)
    :param nullable: valeur nulle autorisée
    :param default: valeur par defaut
    :param primary_key: valeur de cle primaire
    :param unique: valeur unique
    :param editable: valeur editable
    :param check: fonction de validation

    :raise FieldGenomicError: si la séquence n'est pas valide
    :raise FieldGenomicError: si la valeur par defaut n'est pas valide
    :raise FieldGenomicError: si la valeur n'est pas valide

    :return: str
    """

    bases = {
        'DNA': {
            'A', 'T', 'C', 'G'
        },
        'RNA': {
            'A', 'U', 'C', 'G'
        },
        'Protein': {
            'A', 'R', 'N', 'D', 'C',
            'Q', 'E', 'G', 'H', 'I',
            'L', 'K', 'M', 'F', 'P',
            'S', 'T', 'W', 'Y', 'V'
        }
    }

    def __init__(
        self,
        # DNA, RNA, Protein
        sequence: str = 'DNA',
        nullable: bool = True,
        default: str | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        if sequence not in self.bases.keys():
            raise field.FieldGenomicError(f"{sequence} is not a valid sequence")
        self._sequence = sequence
        if default and not callable(default):
            if not all([base in self.bases[sequence] for base in default]):
                raise field.FieldGenomicError(f"{default} is not a valid {sequence} sequence")
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: str) -> str:
        return value

    def dump(self) -> str:
        return self._value

    def _validated(self, value: str) -> bool:
        if not all([base in self.bases[self._sequence] for base in value]):
            return False
        return super()._validated(value)
