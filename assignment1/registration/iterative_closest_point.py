import random
import bpy
import bmesh
import mathutils
import numpy as np
import scipy.spatial

def numpy_verts(mesh: bmesh.types.BMesh) -> np.ndarray:
    data = bpy.data.meshes.new('tmp')
    mesh.to_mesh(data)
    vertices = np.zeros(len(mesh.verts) * 3, dtype=np.float64)
    data.vertices.foreach_get('co', vertices)
    return vertices.reshape([len(mesh.verts), 3])

def numpy_normals(mesh: bmesh.types.BMesh) -> np.ndarray:
    data = bpy.data.meshes.new('tmp')
    mesh.to_mesh(data)
    normals = np.zeros(len(mesh.verts) * 3, dtype=np.float64)
    data.vertices.foreach_get('normal', normals)
    return normals.reshape([len(mesh.verts), 3])

def point_to_point_transformation(source_points, destination_points, **kwargs):
    if len(source_points) == 0 or source_points.shape != destination_points.shape:
        return mathutils.Matrix.Identity(4)

    centroid_source = np.mean(source_points, axis=0)
    centroid_destination = np.mean(destination_points, axis=0)

    H = np.dot((source_points - centroid_source).T, (destination_points - centroid_destination))

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

def point_to_plane_transformation(source_points, destination_points, destination_normals, **kwargs):
    return mathutils.Matrix.Identity(4)

def closest_point_registration(source, destination, k, num_points, distance_metric="POINT_TO_POINT", **kwargs):
    source_points = numpy_verts(source)
    destination_points = numpy_verts(destination)

    if num_points > len(source_points):
        num_points = len(source_points)
    if num_points < 1:
        num_points = 1

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
        return point_to_point_transformation(inlier_source_points, inlier_destination_points)
    elif distance_metric == "POINT_TO_PLANE":
        inlier_destination_normals = numpy_normals(destination)[closest_indices][inliers]
        return point_to_plane_transformation(inlier_source_points, inlier_destination_points, inlier_destination_normals)
    else:
        raise Exception(f"Unrecognized distance metric '{distance_metric}'")


def farthest_point_sampling(point_cloud, num_samples):
    sampled_points = []
    sampled_points.append(point_cloud[np.random.randint(len(point_cloud))])
    distances = np.full(len(point_cloud), np.inf)

    for _ in range(1, num_samples):
        for i, point in enumerate(point_cloud):
            distances[i] = min(distances[i], np.linalg.norm(point - sampled_points[-1]))
        sampled_points.append(point_cloud[np.argmax(distances)])

    return np.array(sampled_points)


def normal_space_sampling(point_cloud, normals, num_samples, num_bins=10):
    bins = np.zeros((num_bins, num_bins, num_bins), dtype=list)
    for i in range(num_bins):
        for j in range(num_bins):
            for k in range(num_bins):
                bins[i][j][k] = []
    def bin_index(normal):
        theta = np.arccos(normal[2]) / np.pi
        phi = (np.arctan2(normal[1], normal[0]) + np.pi) / (2 * np.pi)
        return int(theta * num_bins), int(phi * num_bins), int((theta + phi) * num_bins % num_bins)

    for i, normal in enumerate(normals):
        idx = bin_index(normal)
        bins[idx[0]][idx[1]][idx[2]].append(point_cloud[i])

    sampled_points = []
    bin_indices = np.array([[i, j, k] for i in range(num_bins) for j in range(num_bins) for k in range(num_bins)])
    np.random.shuffle(bin_indices)

    for idx in bin_indices:
        if len(bins[idx[0]][idx[1]][idx[2]]) > 0:
            sampled_points.append(random.choice(bins[idx[0]][idx[1]][idx[2]]))
        if len(sampled_points) >= num_samples:
            break

    return np.array(sampled_points)

def iterative_closest_point_registration_with_sampling(source, destination, k, num_points, iterations, epsilon,
                                                       distance_metric="POINT_TO_POINT", sampling_method="FPS",
                                                       **kwargs):
    transformations = []
    for _ in range(iterations):
        if sampling_method == "FPS":
            source_sampled_points = farthest_point_sampling(source_points, num_points)
        elif sampling_method == "NORMAL_SPACE":
            source_sampled_points = normal_space_sampling(source_points, source_normals, num_points)
        else:
            raise ValueError("Unsupported sampling method")

        transformation = closest_point_registration(source_sampled_points, destination, k, num_points, distance_metric,
                                                    **kwargs)
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
