import random
import bpy
import bmesh
import mathutils
import numpy as np
import scipy.spatial
from sklearn.cluster import KMeans


def numpy_verts(mesh: bmesh.types.BMesh) -> np.ndarray:
    data = bpy.data.meshes.new("tmp")
    mesh.to_mesh(data)
    vertices = np.zeros(len(mesh.verts) * 3, dtype=np.float64)
    data.vertices.foreach_get("co", vertices)
    return vertices.reshape([len(mesh.verts), 3])


def numpy_normals(mesh: bmesh.types.BMesh) -> np.ndarray:
    data = bpy.data.meshes.new("tmp")
    mesh.to_mesh(data)
    normals = np.zeros(len(mesh.verts) * 3, dtype=np.float64)
    data.vertices.foreach_get("normal", normals)
    return normals.reshape([len(mesh.verts), 3])


def point_to_point_transformation(source_points, destination_points, **kwargs):
    if len(source_points) == 0 or source_points.shape != destination_points.shape:
        return mathutils.Matrix.Identity(4)

    centroid_source = np.mean(source_points, axis=0)
    centroid_destination = np.mean(destination_points, axis=0)

    H = np.dot(
        (source_points - centroid_source).T, (destination_points - centroid_destination)
    )

    U, S, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = np.dot(Vt.T, U.T)

    T = centroid_destination.T - np.dot(R, centroid_source.T)

    transformation = mathutils.Matrix.Identity(4)
    for i in range(3):
        for j in range(3):
            transformation[i][j] = R[i, j]
        transformation[i][3] = T[i]

    return transformation


# !!! This function will be used for automatic grading, don't edit the signature !!!
def point_to_plane_transformation(
    source_points: np.ndarray,
    destination_points: np.ndarray,
    destination_normals: np.ndarray,
    **kwargs,
) -> mathutils.Matrix:
    """
    Given a set of point-pairs, finds an approximate transformation to register source points to destination points.

    Here, the destination point are supplemented with normals.
    Instead of moving the source points toward each destination point,
    we can instead move them toward the planes defined by each destination point and its normal.

    Point pairs and normals are passed as three separate matrices of the same shape, associations are made index-wise:
        source_points[i, :] --> destination_points[i, :], destination_normals[i, :]

    :param source_points: Collection of n points to move, represented by an [n, 3] numpy matrix.
    :param destination_points: Collection of n points to move toward, represented by an [n, 3] numpy matrix.
    :param destination_normals: Collection of n normals of the destination points, represented by an [n, 3] numpy matrix.
    :return: A transformation matrix which, applied to every point in source_points,
             would bring them closer to being registered with destination_points.
             The transformation should contain only translation and rotation components;
             this version of rigid registration should not re-scale the source mesh.
    """
    A = np.zeros((len(source_points), 6))
    b = np.zeros((len(source_points), 1))

    for i in range(len(source_points)):
        p_s = source_points[i]
        p_d = destination_points[i]
        n_d = destination_normals[i]

        cross_prod = np.cross(p_s, n_d)

        A[i, 0:3] = cross_prod
        A[i, 3:6] = n_d
        b[i, 0] = np.dot(n_d, p_d - p_s)

    # Solve the linear system using least squares
    x, resids, rank, s = np.linalg.lstsq(A, b, rcond=None)

    rotation_vector = x[0:3]
    translation_vector = x[3:6]

    # Construct the rotation matrix from the rotation vector
    angle = np.linalg.norm(rotation_vector)
    if angle != 0:
        axis = rotation_vector / angle
        R = mathutils.Matrix.Rotation(angle, 4, mathutils.Vector(axis))
    else:
        R = mathutils.Matrix.Identity(4)

    # Construct the translation matrix from the translation vector
    T = mathutils.Matrix.Translation(translation_vector.flatten())

    # Combine rotation and translation into a single transformation matrix
    transformation = T @ R

    return transformation


def farthest_point_sampling(points, num_samples):
    selected_indices = [np.random.randint(len(points))]
    selected_points = [points[selected_indices[-1]]]

    distances = np.full(len(points), np.inf)

    for _ in range(1, num_samples):
        last_point = selected_points[-1]
        dists = np.linalg.norm(points - last_point, axis=1)
        distances = np.minimum(distances, dists)
        farthest_index = np.argmax(distances)

        selected_indices.append(farthest_index)
        selected_points.append(points[farthest_index])

    return np.array(selected_points), np.array(selected_indices)


def normal_space_sampling(points, normals, num_samples, num_clusters=10):
    # Ensure the number of clusters does not exceed the number of points
    num_clusters = min(num_clusters, len(points))

    # Normalize the normals to unit length
    normalized_normals = normals / np.linalg.norm(normals, axis=1, keepdims=True)

    # Use k-means clustering to cluster normals
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=num_clusters)
    labels = kmeans.fit_predict(normalized_normals)

    # Select points from each cluster
    cluster_indices = [np.where(labels == i)[0] for i in range(num_clusters)]

    sampled_indices = []
    for indices in cluster_indices:
        if len(indices) > 0:
            sampled_indices.extend(
                np.random.choice(
                    indices,
                    min(len(indices), num_samples // num_clusters),
                    replace=False,
                )
            )

    if len(sampled_indices) < num_samples:
        additional_indices = np.random.choice(
            len(points), num_samples - len(sampled_indices), replace=False
        )
        sampled_indices.extend(additional_indices)

    return points[sampled_indices], sampled_indices


SAMPLING_METHOD = "NORMAL_SPACE"


def closest_point_registration(
    source, destination, k, num_points, distance_metric="POINT_TO_POINT", **kwargs
):
    source_points = numpy_verts(source)
    destination_points = numpy_verts(destination)

    if num_points > len(source_points):
        num_points = len(source_points)
    if num_points < 1:
        num_points = 1
    if SAMPLING_METHOD == "FPS":
        selected_source_points, selected_indices = farthest_point_sampling(
            source_points, num_points
        )
    elif SAMPLING_METHOD == "NORMAL_SPACE":
        source_normals = numpy_normals(source)
        selected_source_points, selected_indices = normal_space_sampling(
            source_points, source_normals, num_points
        )
    else:
        indices = np.random.choice(len(source_points), num_points, replace=False)
        selected_source_points = source_points[indices]

    destination_tree = scipy.spatial.KDTree(destination_points)
    distances, closest_indices = destination_tree.query(selected_source_points)
    selected_destination_points = destination_points[closest_indices]

    median_distance = np.median(distances)
    inliers = distances < k * median_distance

    inlier_source_points = selected_source_points[inliers]
    inlier_destination_points = selected_destination_points[inliers]

    if distance_metric == "POINT_TO_POINT":
        return point_to_point_transformation(
            inlier_source_points, inlier_destination_points
        )
    elif distance_metric == "POINT_TO_PLANE":
        inlier_destination_normals = numpy_normals(destination)[closest_indices][
            inliers
        ]
        return point_to_plane_transformation(
            inlier_source_points, inlier_destination_points, inlier_destination_normals
        )
    else:
        raise Exception(f"Unrecognized distance metric '{distance_metric}'")


def iterative_closest_point_registration(
    source,
    destination,
    k,
    num_points,
    iterations,
    epsilon,
    distance_metric="POINT_TO_POINT",
    **kwargs,
):
    transformations = []
    for _ in range(iterations):
        transformation = closest_point_registration(
            source, destination, k, num_points, distance_metric, **kwargs
        )
        deviation = np.asarray(transformation - mathutils.Matrix.Identity(4))
        if np.linalg.norm(deviation) < epsilon and np.max(deviation) < epsilon:
            break
        source.transform(transformation)
        transformations.append(transformation)
    return transformations


def net_transformation(transformations):
    m = mathutils.Matrix.Identity(4)
    for t in transformations:
        m = t @ m
    return m
