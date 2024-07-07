"""
ALL MAPPING FIELDS TEST
"""
import unittest
from core.models import (
    Model,
    AggregationField,
    ArrayField,
    GeographicalField,
    MatrixField
)


class User(Model):
    # note par matiere
    notes = AggregationField()


def verify(data):
    for item in data:
        if 'r' not in item[0]:
            return False
    return True


class Food(Model):
    foods = AggregationField(
        check=verify,
        functions={'length': (lambda name : len(name))}
    )


class TestAggregationField(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(notes=[("his-geo", 14), ("fran", 18), ("svt", 11.5), ("math", 2.2)])
        self.eat = Food(foods=(("rice", 5), ('burger', 12)))

    def test_todict(self):
        self.assertIsInstance(self.user.mapping, dict)
        self.assertEqual(len(self.user.mapping), 1)
        self.assertIn('notes', self.user.mapping)

    def test_value(self):
        self.assertEqual(
            self.user.notes,
            [("his-geo", 14), ("fran", 18), ("svt", 11.5), ("math", 2.2)]
        )
        self.assertEqual(
            User.notes.load(
                User.notes.dump(
                    self.user.notes
                )
            ),
            self.user.notes
        )

    def test_func(self):
        self.assertTrue(hasattr(Food.foods, 'length'))
        self.assertEqual(Food.foods.length(self.eat.foods[0][0]), 4)


class Fruits(Model):
    names = ArrayField()


class TestArrayField(unittest.TestCase):
    def setUp(self) -> None:
        self.array = Fruits(names=["mangoes", "bananas", "apples"])

    def test_value(self):
        self.assertEqual(
            self.array.names,
            ["mangoes", "bananas", "apples"]
        )
        self.assertEqual(
            Fruits.names.load(
                Fruits.names.dump(
                    self.array.names
                )
            ),
            self.array.names
        )


class Coordinates(Model):
    coordinates = GeographicalField()


class TestGeographicalField(unittest.TestCase):
    def setUp(self) -> None:
        self.geo = Coordinates(coordinates=(0.0, 0.0))

    def test_value(self):
        self.assertEqual(
            (self.geo.coordinates.lat, self.geo.coordinates.lng),
            (0.0, 0.0)
        )
        self.assertEqual(
            Coordinates.coordinates.load(
                Coordinates.coordinates.dump(
                    (self.geo.coordinates.lat, self.geo.coordinates.lng)
                )
            ),
            self.geo.coordinates
        )


class classRoom(Model):
    matrix = MatrixField()


class TestMatrixField(unittest.TestCase):
    def setUp(self) -> None:
        self.mat = classRoom(matrix=[[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    def test_value(self):
        self.assertEqual(
            self.mat.matrix,
            [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        )
        self.assertEqual(
            classRoom.matrix.load(
                classRoom.matrix.dump(
                    self.mat.matrix
                )
            ),
            self.mat.matrix
        )
