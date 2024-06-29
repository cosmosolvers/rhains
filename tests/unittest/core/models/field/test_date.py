"""
ALL DATE FIELDS TEST
"""
import unittest
import datetime
from core.models import (
    Model,
    DateField,
    DateTimeField,
    TimeField
)
from exceptions.core.models import field


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
        self.assertEqual(Meet.hours._format, '%Y-%m-%d')
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
    time = DateTimeField(primary_key=True, default="2024-09-17 10:30:00")


class TestDateTimeField(unittest.TestCase):
    def setUp(self) -> None:
        self.school = School()

    def test_attrs(self):
        self.assertEqual(self.school.time, datetime.datetime(2024, 9, 17, 10, 30, 0))

    def test_format(self):
        with self.assertRaises(field.DateTimeFieldValidationError):
            self.school.time = "2024-02-18"
            self.school.time = "2024-20-18 10:30:00"

    def test_parse(self):
        old = self.school.time
        self.school.time = School.time.dump(old)
        self.assertEqual(self.school.time, old)
        data = School.time.load(School.time.dump(old))
        self.assertEqual(self.school.time, data)


class Daily(Model):
    now = TimeField()


class TestTimeField(unittest.TestCase):
    def setUp(self) -> None:
        self.daily = Daily(now="23:30:01")

    def test_attrs(self):
        self.assertEqual(self.daily.now, datetime.time(23, 30, 1))

    def test_format(self):
        with self.assertRaises(field.TimeFieldParseError):
            self.daily.now = "213"
            self.daily.now = "21:666"
