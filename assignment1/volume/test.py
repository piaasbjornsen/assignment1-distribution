import unittest
from .volume import mesh_volume
from data import primitives, meshes


class TestVolume(unittest.TestCase):

    # HINT: Add your own unit tests here
    def test_double_toroid(self):
        self.assertEqual(
            mesh_volume(meshes.DOUBLE_TORUS), 2.3324, "The double toroid should have volume 2.3324"
        )

    def test_bagel_cut_torus(self):
        self.assertEqual(
            mesh_volume(meshes.BAGEL_CUT_TORUS),
            -1,
            "The bagel cut torus should have volume -1",
        )

    def test_half_bagel_cut_torus(self):
        self.assertEqual(
            mesh_volume(meshes.HALF_BAGEL_CUT_TORUS),
            -1,
            "The half bagel cut torus should have volume -1",
        )

    def test_half_torus(self):
        self.assertEqual(
            mesh_volume(meshes.HALF_TORUS), -1, "The half torus should have volume -1"
        )

    def test_two_tori(self):
        self.assertEqual(
            mesh_volume(meshes.TWO_TORI),
            2.3494,
            "The two tori should have volume 2.3494",
        )
