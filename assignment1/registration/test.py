import random
import unittest
from .iterative_closest_point import *
from data import primitives, meshes
import mathutils

NUM_TESTS = 10


class TestRegistration(unittest.TestCase):

    def assertSimilarTransformations(self, a: mathutils.Matrix, b: mathutils.Matrix):
        translation_error = a.to_translation() - b.to_translation()
        self.assertAlmostEqual(
            translation_error.magnitude, 0, 3,
            "Translation error should be low"
        )
        rotation_error = a.to_quaternion() - b.to_quaternion()
        self.assertAlmostEqual(
            rotation_error.magnitude, 0, 3,
            "Rotation error should be low"
        )
        scaling_error = a.to_scale() - b.to_scale()
        self.assertAlmostEqual(
            scaling_error.magnitude, 0, 3,
            "Scaling should be zero"
        )

    def test_cube(self):
        translation = mathutils.Matrix.Translation([
            random.uniform(-0.01, 0.01),
            random.uniform(-0.01, 0.01),
            random.uniform(-0.01, 0.01)
        ])
        rotation = mathutils.Matrix.Rotation(random.uniform(-0.01, 0.01), 4, 'X') \
                   @ mathutils.Matrix.Rotation(random.uniform(-0.01, 0.01), 4, 'Y') \
                   @ mathutils.Matrix.Rotation(random.uniform(-0.01, 0.01), 4, 'Z')
        transformation = translation @ rotation

        source, destination = primitives.CUBE, primitives.CUBE.copy()
        destination.transform(transformation)  # Move the destination, so we don't need to invert the transform

        registration_transformations = iterative_closest_point_registration(
            source, destination,
            k=2.5, num_points=4096,
            iterations=100, epsilon=0.0005,
            distance_metric='POINT_TO_POINT'
        )

        # The function should have converged
        self.assertLess(len(registration_transformations), 100)

        # Check that we found the right matrix
        estimated_transformation = net_transformation(registration_transformations)
        self.assertSimilarTransformations(transformation, estimated_transformation)

    # TODO: Add unit tests for ICP


    # HINT: You can generate test-cases by applying a random transformation to a mesh
    #       and checking if ICP can 'undo' the transformation

    # HINT: Start by testing (small) random translations of different primitives

    # HINT: Once your method works for translations, test (small) random rotations

    # HINT: Finally, make sure your method works for transformations with both a translation and a rotation component
