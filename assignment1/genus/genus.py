import bmesh
from assignment1.boundaries import mesh_boundary_loops
from assignment1.components import mesh_connected_components


# !!! This function will be used for automatic grading, don't edit the signature !!!
def mesh_genus(mesh: bmesh.types.BMesh) -> int:
    """
    Finds the genus of a mesh.

    Assuming the mesh represents a manifold surface (no boundary loops),
    this function should return the number of "holes" in the surface.
    e.g. A sphere or a cube has genus 0, a toroid has genus 1, a double toroid has genus 2.

    BONUS: Account for non-manifold meshes by treating each boundary loop (hole) as one face.

    :param mesh: The mesh to find the genus of.
    :return: The genus of the mesh, as an integer.
    """
    # TODO: This should return the genus of the mesh
    num_components = len(mesh_connected_components(mesh))
    num_loops = len(mesh_boundary_loops(mesh))

    if num_components > 1 and num_loops == 0:
        return -1

    V = len(mesh.verts)
    E = len(mesh.edges)
    F = len(mesh.faces)

    # Formula to calculate genus
    genus = 1 - (V - E + F) // 2
    return genus
