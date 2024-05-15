import bmesh


def is_mesh_closed(mesh):
    edge_face_count = {}
    for edge in mesh.edges:
        for face in edge.link_faces:
            edge_face_count[edge] = edge_face_count.get(edge, 0) + 1

    # If any edge is linked to fewer than or more than 2 faces, the mesh is open
    return all(count == 2 for count in edge_face_count.values())

def mesh_volume(mesh: bmesh.types.BMesh) -> float:
    """
    Finds the volume of the mesh.

    NOTE: the use of `mesh.calc_volume()` is not permitted inside this function!
          This task is intended to be completed manually, using methods discussed in class.

    :param mesh: The mesh to find the volume of.
    :return: The volume of the mesh as a float.
    """

    # Use this in your main function
    if not is_mesh_closed(mesh):
        return -1  # Return zero volume for open meshes

    # (The math is a lot simpler if you know you only need to work with triangular faces)
    bmesh.ops.triangulate(mesh, faces=mesh.faces)

    # TODO: Return the volume of the mesh (without using Blender's built-in functionality)
    # Calculate the volume contribution of each triangle
    volume = 0.0
    for face in mesh.faces:
        v0 = face.verts[0].co
        v1 = face.verts[1].co
        v2 = face.verts[2].co

        # Compute the signed volume of the tetrahedron formed by the face and the origin
        vol = v0.dot(v1.cross(v2)) / 6.0
        volume += vol

    result = abs(volume)
    truncated_result = int(result * 10000) / 10000.0

    return truncated_result  # Return the absolute volume to ensure positivity
