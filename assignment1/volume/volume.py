import bmesh


# !!! This function will be used for automatic grading, don't edit the signature !!!
def mesh_volume(mesh: bmesh.types.BMesh) -> float:
    """
    Finds the volume of the mesh.

    NOTE: the use of `mesh.calc_volume()` is not permitted inside this function!
          This task is intended to be completed manually, using methods discussed in class.

    :param mesh: The mesh to find the volume of.
    :return: The volume of the mesh as a float.
    """

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

    return result  # Return the absolute volume to ensure positivity
