"""
TEST FIELD
"""
import unittest
from typing import Callable, Any
from core.models.field import field as fd
from exception.core.models import field


class Inheritance(fd.Field):
    def __init__(
        self,
        nullable: bool = True,
        default: Any | None = None,
        primary_key: bool = False,
        unique: bool = False,
        editable: bool = True,
        check: Callable[..., Any] | None = None
    ):
        super().__init__(
            nullable,
            default,
            primary_key,
            unique,
            editable,
            check
        )

    def load(self, value: Any) -> Any:
        return value

    def dump(self) -> Any:
        return self._value


class TestSuccesField(unittest.TestCase):

    def test_instance(self):
        instance = Inheritance()
        self.assertIsInstance(instance, fd.Field)

    def test_class(self):
        instance = Inheritance()
        self.assertEqual(instance._nullable, True)
        self.assertEqual(instance._editable, True)
        self.assertEqual(instance._unique, False)

    def test_with_value(self):
        instance = Inheritance()
        instance.__set__(instance, 7)
        self.assertEqual(instance._value, 7)
        self.assertIsInstance(instance, Inheritance)

    def test_with_nullable(self):
        instance = Inheritance(nullable=False, default=5)
        self.assertEqual(instance.load("fatou"), "fatou")
        self.assertEqual(instance.dump(), 5)

    def test_with_primarykey(self):
        instance = Inheritance(primary_key=True, default="moi-meme", nullable=False)
        self.assertEqual(instance.load(1.8), 1.8)
        self.assertEqual(instance.dump(), "moi-meme")

    def test_with_editable(self):
        instance = Inheritance(editable=False, default="moi-meme")
        self.assertEqual(instance.load(1.8), 1.8)
        self.assertEqual(instance.dump(), "moi-meme")

    def test_with_unique(self):
        instance = Inheritance(unique=True, default="moi-meme", nullable=False)
        self.assertEqual(instance.load(1.8), 1.8)
        self.assertEqual(instance.dump(), "moi-meme")

    def test_with_check(self):
        instance = Inheritance(check=lambda x: x > 0, default=5)
        self.assertEqual(instance.load(1.8), 1.8)
        self.assertEqual(instance.dump(), 5)


class TestErrorFieldWithNullable(unittest.TestCase):

    def test_by_not_default(self):
        with self.assertRaises(field.FieldDefaultError) as err:
            Inheritance(nullable=False)
            self.assertEqual(err.msg, "default value is required")

    def test_by_not_editable(self):
        with self.assertRaises(field.FieldDefaultError) as err:
            Inheritance(nullable=False, editable=False)
            self.assertEqual(err.msg, "default value is required")

    def test_by_primarykey(self):
        with self.assertRaises(field.FieldDefaultError) as err:
            Inheritance(nullable=False, primary_key=True)
            self.assertEqual(err.msg, "default value is required")

    def test_by_not_unique(self):
        with self.assertRaises(field.FieldUniqueError) as err:
            Inheritance(unique=True)
            self.assertEqual(err.msg, "nullable field can't be unique")


class TestErrorFieldWithPrimarykey(unittest.TestCase):

    def test_by_nullable(self):
        with self.assertRaises(field.FieldPrimarykeyError) as err:
            Inheritance(primary_key=True, nullable=True)
            self.assertEqual(err.msg, "nullable field can't be primary key")


class TestErrorFieldWithCheck(unittest.TestCase):

    def test_by_not_callable(self):
        with self.assertRaises(field.FieldCheckError) as err:
            Inheritance(check="lambda x: x > 0")
            self.assertEqual(err.msg, "lambda x: x > 0 is not a valid function")

    def test_by_not_valid_function(self):
        with self.assertRaises(field.FieldCheckError) as err:
            Inheritance(check=lambda x, y: x + y)
            self.assertEqual(err.msg, "lambda x: x > 0 is not a valid function")


class TestErrorFieldEditable(unittest.TestCase):

    def test_by_not_callable(self):
        test = Inheritance(editable=False, default="lambda x: x > 0")
        test = test.__set__(test, 5)


if __name__ == "__main__":
    unittest.main()
