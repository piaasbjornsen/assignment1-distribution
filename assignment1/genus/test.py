import unittest
from .genus import mesh_genus
from data import primitives, meshes


class TestGenus(unittest.TestCase):

    def test_cube(self):
        self.assertEqual(mesh_genus(primitives.CUBE), 0, "Cube should have genus 0")

    def test_toroid(self):
        self.assertEqual(mesh_genus(primitives.TORUS), 1, "Toroid should have genus 1")

    def test_double_toroid(self):
        self.assertEqual(mesh_genus(meshes.DOUBLE_TORUS), 2, "The double toroid should have genus 2")

