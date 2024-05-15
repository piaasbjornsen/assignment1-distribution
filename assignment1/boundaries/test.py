import bpy
import bmesh
import unittest
from .boundary_loops import mesh_boundary_loops
from data import primitives, meshes


class TestBoundaries(unittest.TestCase):
    # HINT: add some unit tests!
    def test_double_toroid(self):
        self.assertEqual(
            len(mesh_boundary_loops(meshes.DOUBLE_TORUS)), 0, "The double toroid should have 0 boundary loops"
        )

    def test_bagel_cut_torus(self):
        self.assertEqual(
            len(mesh_boundary_loops(meshes.BAGEL_CUT_TORUS)),
            4,
            "The bagel cut torus should have 4 boundary loops ",
        )

    def test_half_bagel_cut_torus(self):
        self.assertEqual(
            len(mesh_boundary_loops(meshes.HALF_BAGEL_CUT_TORUS)),
            2,
            "The half bagel cut torus should have 2 boundary loops",
        )

    def test_half_torus(self):
        self.assertEqual(
            len(mesh_boundary_loops(meshes.HALF_TORUS)), 2, "The half torus should have 2 boundary loops"
        )

    def test_two_tori(self):
        self.assertEqual(
            len(mesh_boundary_loops(meshes.TWO_TORI)),
            0,
            "The two tori should have 0 boundary loops",
        )

