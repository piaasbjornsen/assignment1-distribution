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

def iterative_closest_point_registration(source, destination, k, num_points, iterations, epsilon, distance_metric="POINT_TO_POINT", **kwargs):
    transformations = []
    for _ in range(iterations):
        transformation = closest_point_registration(source, destination, k, num_points, distance_metric, **kwargs)
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
