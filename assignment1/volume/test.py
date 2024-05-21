import unittest
from .volume import mesh_volume
from data import primitives, meshes


class TestVolume(unittest.TestCase):

    # HINT: Add your own unit tests here
    def test_double_toroid(self):
        self.assertEqual(
            mesh_volume(meshes.DOUBLE_TORUS),
            2.3324,
            "The double toroid should have volume 2.3324",
        )

    def test_two_tori(self):
        self.assertEqual(
            mesh_volume(meshes.TWO_TORI),
            2.3494,
            "The two tori should have volume 2.3494",
        )
