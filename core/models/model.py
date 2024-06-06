"""
"""
from typing import Self
import uuid

from .field.charfield import CharField

from core.rh.collection import Collection


class Model:
    collection = Collection(Self)
    pk = CharField(default=uuid.uuid4)

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    class Meta:
        database = 'default'
        # dict or scalar
        result = 'dict'
        abstract = False
