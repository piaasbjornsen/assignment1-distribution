import random
import unittest
from .iterative_closest_point import *
from data import primitives
import mathutils

NUM_TESTS = 10


class TestRegistration(unittest.TestCase):

    def assertSimilarTransformations(self, a: mathutils.Matrix, b: mathutils.Matrix):
        translation_error = a.to_translation() - b.to_translation()
        self.assertAlmostEqual(
            translation_error.magnitude, 0, 3, "Translation error should be low"
        )
        rotation_error = a.to_quaternion() - b.to_quaternion()
        self.assertAlmostEqual(
            rotation_error.magnitude, 0, 3, "Rotation error should be low"
        )
        scaling_error = a.to_scale() - b.to_scale()
        self.assertAlmostEqual(scaling_error.magnitude, 0, 3, "Scaling should be zero")

    def generate_random_translation(self):
        return mathutils.Matrix.Translation(
            [
                random.uniform(-0.01, 0.01),
                random.uniform(-0.01, 0.01),
                random.uniform(-0.01, 0.01),
            ]
        )

    def generate_random_rotation(self):
        return (
            mathutils.Matrix.Rotation(random.uniform(-0.01, 0.01), 4, "X")
            @ mathutils.Matrix.Rotation(random.uniform(-0.01, 0.01), 4, "Y")
            @ mathutils.Matrix.Rotation(random.uniform(-0.01, 0.01), 4, "Z")
        )

    def test_primitive_translation_point_to_point(self):
        for primitive in primitives.ALL_PRIMITIVES:
            for _ in range(NUM_TESTS):
                translation = self.generate_random_translation()
                source, destination = primitive.copy(), primitive.copy()
                destination.transform(translation)

                registration_transformations = iterative_closest_point_registration(
                    source,
                    destination,
                    k=2.5,
                    num_points=4096,
                    iterations=100,
                    epsilon=0.0005,
                    distance_metric="POINT_TO_POINT",
                )

                self.assertLess(len(registration_transformations), 100)
                estimated_transformation = net_transformation(
                    registration_transformations
                )
                self.assertSimilarTransformations(translation, estimated_transformation)

    def test_primitive_rotation_point_to_point(self):
        for primitive in primitives.ALL_PRIMITIVES:
            for _ in range(NUM_TESTS):
                rotation = self.generate_random_rotation()
                source, destination = primitive.copy(), primitive.copy()
                destination.transform(rotation)

                registration_transformations = iterative_closest_point_registration(
                    source,
                    destination,
                    k=2.5,
                    num_points=4096,
                    iterations=100,
                    epsilon=0.0005,
                    distance_metric="POINT_TO_POINT",
                )

                self.assertLess(len(registration_transformations), 100)
                estimated_transformation = net_transformation(
                    registration_transformations
                )
                self.assertSimilarTransformations(rotation, estimated_transformation)

    def test_primitive_combined_transform_point_to_point(self):
        for primitive in primitives.ALL_PRIMITIVES:
            for _ in range(NUM_TESTS):
                translation = self.generate_random_translation()
                rotation = self.generate_random_rotation()
                combined_transform = translation @ rotation

                source, destination = primitive.copy(), primitive.copy()
                destination.transform(combined_transform)

                registration_transformations = iterative_closest_point_registration(
                    source,
                    destination,
                    k=2.5,
                    num_points=4096,
                    iterations=100,
                    epsilon=0.0005,
                    distance_metric="POINT_TO_POINT",
                )

                self.assertLess(len(registration_transformations), 100)
                estimated_transformation = net_transformation(
                    registration_transformations
                )
                self.assertSimilarTransformations(
                    combined_transform, estimated_transformation
                )

    def test_primitive_translation_point_to_plane(self):
        for primitive in primitives.ALL_PRIMITIVES:
            for _ in range(NUM_TESTS):
                translation = self.generate_random_translation()
                source, destination = primitive.copy(), primitive.copy()
                destination.transform(translation)

                registration_transformations = iterative_closest_point_registration(
                    source,
                    destination,
                    k=2.5,
                    num_points=4096,
                    iterations=100,
                    epsilon=0.0005,
                    distance_metric="POINT_TO_PLANE",
                )

                self.assertLess(len(registration_transformations), 100)
                estimated_transformation = net_transformation(
                    registration_transformations
                )
                self.assertSimilarTransformations(translation, estimated_transformation)

    def test_primitive_rotation_point_to_plane(self):
        for primitive in primitives.ALL_PRIMITIVES:
            for _ in range(NUM_TESTS):
                rotation = self.generate_random_rotation()
                source, destination = primitive.copy(), primitive.copy()
                destination.transform(rotation)

                registration_transformations = iterative_closest_point_registration(
                    source,
                    destination,
                    k=2.5,
                    num_points=4096,
                    iterations=100,
                    epsilon=0.0005,
                    distance_metric="POINT_TO_PLANE",
                )

                self.assertLess(len(registration_transformations), 100)
                estimated_transformation = net_transformation(
                    registration_transformations
                )
                self.assertSimilarTransformations(rotation, estimated_transformation)

    def test_primitive_combined_transform_point_to_plane(self):
        for primitive in primitives.ALL_PRIMITIVES:
            for _ in range(NUM_TESTS):
                translation = self.generate_random_translation()
                rotation = self.generate_random_rotation()
                combined_transform = translation @ rotation

                source, destination = primitive.copy(), primitive.copy()
                destination.transform(combined_transform)

                registration_transformations = iterative_closest_point_registration(
                    source,
                    destination,
                    k=2.5,
                    num_points=4096,
                    iterations=100,
                    epsilon=0.0005,
                    distance_metric="POINT_TO_PLANE",
                )

                self.assertLess(len(registration_transformations), 100)
                estimated_transformation = net_transformation(
                    registration_transformations
                )
                self.assertSimilarTransformations(
                    combined_transform, estimated_transformation
                )

    # TODO: Add unit tests for ICP

    # HINT: You can generate test-cases by applying a random transformation to a mesh
    #       and checking if ICP can 'undo' the transformation

    # HINT: Start by testing (small) random translations of different primitives

    # HINT: Once your method works for translations, test (small) random rotations

    # HINT: Finally, make sure your method works for transformations with both a translation and a rotation component
