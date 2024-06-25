"""
ALL DATE FIELDS TEST
"""
import unittest
import datetime
from core.models import (
    Model,
    DateField,
    DateTimeField,
    DateTimeOffSetField,
    TimeField
)
from exception.core.models import field


class Meet(Model):
    hours = DateField(nullable=False, default="2024-07-05")


class Birth(Model):
    date = DateField(auto_created=True, editable=False)


class TestDateField(unittest.TestCase):
    def setUp(self) -> None:
        self.meet = Meet()
        self.birth = Birth()

    def test_attrs(self):
        self.assertEqual(self.meet.hours, datetime.datetime(2024, 7, 5))
        self.assertEqual(Meet.hours._format[0], '%Y-%m-%d')
        self.assertIsNot(self.birth.date, None)

    def test_error_format(self):
        with self.assertRaises(field.DateFieldValidationError):
            self.meet.hours = datetime.datetime.now().isoformat()

    def test_error_editable(self):
        with self.assertRaises(field.FieldEditableError):
            self.birth.date = datetime.datetime.now()

    def test_parse(self):
        old = self.meet.hours
        self.meet.hours = Meet.hours.dump(self.meet.hours)
        self.assertEqual(self.meet.hours, old)
        data = Meet.hours.load(Meet.hours.dump(self.meet.hours))
        self.assertEqual(self.meet.hours, data)


class School(Model):
    time = DateTimeField()

class TestDateTimeField(unittest.TestCase):
    pass


class TestDateTimeOffSetField(unittest.TestCase):
    pass


class TestTimeField(unittest.TestCase):
    pass
