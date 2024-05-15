import unittest
from .connected_components import mesh_connected_components
from data import primitives, meshes


class TestConnectedComponents(unittest.TestCase):

    # HINT: Add unit tests for simple primitives (one connected component)

    # HINT: Add unit tests for multiple connected components
    #       (You can create examples in the Blender UI by selecting multiple objects and pressing CTRl-J)

    # HINT: Add automated testing of larger component counts, automatically generate examples by combining primitives
    def test_double_toroid(self):
        self.assertEqual(
            len(mesh_connected_components(meshes.DOUBLE_TORUS)), 1, "The double toroid should have 1 component"
        )

    def test_bagel_cut_torus(self):
        self.assertEqual(
            len(mesh_connected_components(meshes.BAGEL_CUT_TORUS)),
            2,
            "The bagel cut torus should have 2 components",
        )

    def test_half_bagel_cut_torus(self):
        self.assertEqual(
            len(mesh_connected_components(meshes.HALF_BAGEL_CUT_TORUS)),
            1,
            "The half bagel cut torus should have 1 component",
        )

    def test_half_torus(self):
        self.assertEqual(
            len(mesh_connected_components(meshes.HALF_TORUS)), 1, "The half torus should have 1 component"
        )

    def test_two_tori(self):
        self.assertEqual(
            len(mesh_connected_components(meshes.TWO_TORI)),
            2,
            "The two tori should have 2 components",
        )

