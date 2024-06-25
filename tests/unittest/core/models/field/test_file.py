"""
ALL FILES FIELDS TEST
"""
import unittest
from core.models import (
    Model,
    AudioField,
    FileField,
    ImageField,
    MediaField
)


class Music(Model):
    jazz = AudioField()


class TestAudioField(unittest.TestCase):
    def setUp(self) -> None:
        self.music = Music(jazz="")


class TestFileField(unittest.TestCase):
    pass


class TestImageField(unittest.TestCase):
    pass


class TestMediaField(unittest.TestCase):
    pass
