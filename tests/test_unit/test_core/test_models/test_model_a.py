"""
MODEL TEST FIELD START WITH A
"""
import unittest
from core.models import (
    Model,
    AggregationField,
    ArrayField,
    AudioField
)


class User(Model):
    # note par matiere
    notes = AggregationField()


class Fruits(Model):
    names = ArrayField()


class Music(Model):
    jazz = AudioField()


class TestAggregationField(unittest.TestCase):
    def setUp(self) -> None:
        user = User(notes=[("his-geo", 14), ("fran", 18), ("svt", 11.5), ("math", 2.2)])

    def 


class TestArrayField(unittest.TestCase):
    def setUp(self) -> None:
        array = Fruits(names=["mangoes", "bananas", "apples"])


class TestAudioField(unittest.TestCase):
    def setUp(self) -> None:
        music = Music(jazz="")
