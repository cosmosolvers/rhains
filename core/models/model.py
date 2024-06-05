"""
"""
from typing import Self

from core.rh.connexion import Connexion


class Model:
    connexion = Connexion(Self)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    class Meta:
        database = 'default'
        # dict or scalar
        result = 'dict'
        abstract = False
