"""
ALL BASES FIELD TEST
"""
import unittest
from core.models import (
    Model,
    Base32Field,
    Base64Field,
    Base64UrlField,
    BaseNField,
    HexadecimalField,
    BinaryField
)


class User(Model):
    # note par matiere
    notes = Base32Field()


class TestBase32Field(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(notes="tttttttttttttttttt")

    def test_todict(self):
        self.assertIsInstance(self.user.mapping, dict)
        self.assertEqual(len(self.user.mapping), 1)
        self.assertIn('notes', self.user.mapping)


class Token(Model):
    token = Base64Field()


class TestBase64Field(unittest.TestCase):
    def setUp(self) -> None:
        self.secret = Token(token="ABCD")

    def test_todict(self):
        self.assertIsInstance(self.secret.mapping, dict)
        self.assertEqual(len(self.secret.mapping), 1)
        self.assertIn('token', self.secret.mapping)

    def test_value(self):
        self.assertEqual(self.secret.token, "ABCD")
        self.assertEqual(Token.token.load(Token.token.dump(self.secret.token)), self.secret.token)


class Url(Model):
    url = Base64UrlField()


class TestBase64UrlField(unittest.TestCase):
    def setUp(self) -> None:
        self.link = Url(url="ABCD")

    def test_todict(self):
        self.assertIsInstance(self.link.mapping, dict)
        self.assertEqual(len(self.link.mapping), 1)
        self.assertIn('url', self.link.mapping)

    def test_value(self):
        self.assertEqual(self.link.url, "ABCD")
        self.assertEqual(Url.url.load(Url.url.dump(self.link.url)), self.link.url)


class TestBaseNField(unittest.TestCase):
    pass


class TestHexadecimalField(unittest.TestCase):
    pass


class TestBinaryField(unittest.TestCase):
    pass
