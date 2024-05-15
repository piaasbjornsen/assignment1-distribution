import bmesh
from assignment1.boundaries import boundary_loops, mesh_boundary_loops
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

    V = len(mesh.verts)
    E = len(mesh.edges)
    F = len(mesh.faces)

    # Debug output to check counts
    print(
        f"Vertices: {V}, Edges: {E}, Faces: {F}, Loops: {num_loops}, Components: {num_components}"
    )

    # Check if there is no boundary loop and no volume (implied by zero faces)
    if num_loops != 0:
        return 0

    # Check if there are more than one component or no boundary loop
    if num_components > 1:
        return -1

    # Adjust Euler characteristic for boundary loops
    euler_characteristic = V - E + F - num_loops

    # Calculate genus using the adjusted Euler characteristic
    genus = (2 * num_components - (euler_characteristic + num_loops)) // 2
    return genus
