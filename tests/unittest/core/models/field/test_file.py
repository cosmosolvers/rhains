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
from core.models.field.file.filefield import MediaView


class Document(Model):
    birth = FileField()


class TestFileField(unittest.TestCase):
    def setUp(self) -> None:
        self.doc = Document(
            birth="/home/hydromel/Downloads/ihm_gtk.pdf"
        )

    def test_verify_data(self):
        self.assertIsInstance(self.doc.birth, MediaView)
        self.assertEqual(
            self.doc.birth.format,
            "PDF"
        )
        self.assertEqual(self.doc.birth.ext, 'pdf')

    def tearDown(self) -> None:
        self.doc.birth.remove()


class Music(Model):
    jazz = AudioField()


class TestAudioField(unittest.TestCase):
    def setUp(self) -> None:
        self.music = Music(
            jazz="/home/hydromel/Downloads/audio_2024-06-30_15-49-01.ogg"
        )

    def test_verify_data(self):
        self.assertIsInstance(self.music.jazz, MediaView)
        self.assertEqual(
            self.music.jazz.format,
            "OGG"
        )
        self.assertEqual(self.music.jazz.ext, 'ogg')

    def tearDown(self) -> None:
        self.music.jazz.remove()


class Picture(Model):
    profile = ImageField()


class TestImageField(unittest.TestCase):
    def setUp(self) -> None:
        self.picture = Picture(
            profile="/home/hydromel/Downloads/Hydromel Victor.png"
        )

    def test_verify_data(self):
        self.assertIsInstance(self.picture.profile, MediaView)
        self.assertEqual(
            self.picture.profile.format,
            "PNG"
        )
        self.assertEqual(self.picture.profile.ext, 'png')

    def tearDown(self) -> None:
        self.picture.profile.remove()


class Video(Model):
    clip = MediaField()


class TestMediaField(unittest.TestCase):
    def setUp(self) -> None:
        self.video = Video(
            clip="/home/hydromel/Downloads/Telegram Desktop/video_2024-06-30_15-49-56.mp4"
        )

    def test_verify_data(self):
        self.assertIsInstance(self.video.clip, MediaView)
        self.assertEqual(
            self.video.clip.format,
            "MP4"
        )
        self.assertEqual(self.video.clip.ext, 'mp4')

    def tearDown(self) -> None:
        self.video.clip.remove()
