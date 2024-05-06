import bmesh
from typing import Optional, List, Set




# !!! This function will be used for automatic grading, don't edit the signature !!!
def mesh_boundary_loops(mesh: bmesh.types.BMesh) -> List[Set[bmesh.types.BMEdge]]:
    """
    Finds the boundary loops of a BMesh.

    Each boundary loop is represented by a `set()` of the edges which make it up.
    Each edge appears in at most one boundary loop.
    Non-boundary edges will not appear in any boundary loops
    HINT: how do you check if an edge is on a boundary?

    :param mesh: The mesh to find the boundary loops of.
    :return: A list of boundary loops, each of which is a set of `BMEdge`s.
    """


    # TODO: Find the boundary loops of the mesh
    loops = []
    visited = set()

    for edge in mesh.edges:
        if edge.is_boundary and edge not in visited:
            loop = set()
            walker = edge.link_loops[0].link_loop_next

            while walker.edge != edge:
                loop.add(walker.edge)
                visited.add(walker.edge)
                walker = walker.link_loop_next
            
            loop.add(edge)  # Add the starting edge to complete the loop
            visited.add(edge)
            loops.append(loop)

    return loops
