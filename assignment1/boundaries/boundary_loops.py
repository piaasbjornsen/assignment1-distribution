import bmesh
from typing import List, Set

def mesh_boundary_loops(mesh: bmesh.types.BMesh) -> List[Set[bmesh.types.BMEdge]]:
    """
    Finds the boundary loops of a BMesh.

    Each boundary loop is represented by a `set()` of the edges which make it up.
    Each edge appears in at most one boundary loop.
    Non-boundary edges will not appear in any boundary loops.

    :param mesh: The mesh to find the boundary loops of.
    :return: A list of boundary loops, each of which is a set of `BMEdge`s.
    """
    loops = []
    visited = set()

    # Loop through all edges in the mesh
    for edge in mesh.edges:
        if edge.is_boundary and edge not in visited:
            # Initialize a new loop
            loop = set()
            current_edge = edge
            # Start a walk from the current edge and keep track of the starting vertex
            start_vertex = current_edge.verts[0]  # Choose the first vertex as the starting point

            while True:
                loop.add(current_edge)
                visited.add(current_edge)

                # Move to the next boundary edge connected to the current edge's other vertex
                next_edge = None
                current_vertex = current_edge.verts[1] if current_edge.verts[0] == start_vertex else current_edge.verts[0]

                # Check all linked edges of the current vertex to find the next boundary edge
                for e in current_vertex.link_edges:
                    if e.is_boundary and e not in visited:
                        next_edge = e
                        break

                # Check if the loop is complete or no unvisited edges are left
                if next_edge is None or next_edge.verts[0] in [current_edge.verts[0], current_edge.verts[1]] and next_edge.verts[1] in [current_edge.verts[0], current_edge.verts[1]]:
                    # Close the loop if it returns to the starting vertex
                    if next_edge and (next_edge.verts[0] == start_vertex or next_edge.verts[1] == start_vertex):
                        loop.add(next_edge)
                        visited.add(next_edge)
                    break

                current_edge = next_edge
                start_vertex = current_vertex  # Update the starting vertex to current vertex for next iteration

            loops.append(loop)

    return loops
