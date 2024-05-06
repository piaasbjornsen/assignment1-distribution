from .connected_components import *
from .test import *

import bpy
import bmesh


class MeshConnectedComponents(bpy.types.Panel):
    # TODO: Add bpy boilerplate (ID name, label, category, etc.)

    # TODO: Add a draw method which uses the function in connected_components.py to show the number of components
    # BONUS: Show the number of points in each connected component
    # BONUS: Include a dropdown which allows the user to select the vertices of each connected component
    bl_idname = "VIEW3D_PT_MeshConnectedComponents"
    bl_label = "Mesh Connected Components"
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
        
        components = mesh_connected_components(bm)
        layout.label(text=f'Number of Components: {len(components)}')
        
        # Bonus: Show details about each component
        for i, comp in enumerate(components):
            layout.label(text=f'Component {i+1}: {len(comp)} vertices')
        
