from .boundary_loops import *
from .test import *

import bpy
import bmesh


class MeshBoundaryLoops(bpy.types.Panel):
    # TODO: Implement a panel which shows the number of boundary loops in the active mesh
    bl_idname = "VIEW3D_PT_MeshBoundaryLoops"
    bl_label = "Mesh Boundary Loops"
    bl_category = "Practical 1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        
        if not obj or obj.type != 'MESH':
            layout.label(text="Select a mesh object.")
            return

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        
        boundary_loops = mesh_boundary_loops(bm)
        layout.label(text=f'Number of Boundary Loops: {len(boundary_loops)}')
        
        # Optionally display details about each boundary loop
        for i, loop in enumerate(boundary_loops):
            layout.label(text=f'Loop {i+1}: {len(loop)} edges')