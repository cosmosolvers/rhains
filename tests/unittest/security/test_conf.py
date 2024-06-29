"""
TEST CONF
"""
import unittest
from core.config.conf import rhconf, Attrs


class TestConf(unittest.TestCase):
    def test_item(self):
        self.assertTrue(hasattr(rhconf, 'project'))
        self.assertTrue(hasattr(rhconf, 'server'))
        self.assertTrue(hasattr(rhconf, 'database'))
        self.assertTrue(hasattr(rhconf, 'media'))

    def test_instance(self):
        self.assertIsInstance(rhconf.project, Attrs)

    def test_sub_item(self):
        self.assertTrue(hasattr(rhconf.project, 'name'))

    def test_setter_item(self):
        rhconf.project.name = 'test'
        rhconf.project.version = 'hydromel'
        rhconf.database.root.user = 'hydromel'
        self.assertEqual(rhconf.project.name, 'test')
        self.assertEqual(rhconf.project.version, 'hydromel')
        self.assertEqual(rhconf.database.root.user, 'hydromel')

    def test_setters(self):
        rhconf.database = {'default': {'engine': 'mysql'}}
        self.assertEqual(rhconf.database.default.engine, 'mysql')
        self.assertEqual(rhconf.database.root.port, 8000)
