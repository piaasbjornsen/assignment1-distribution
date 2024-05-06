from .volume import *
from .test import *

import bpy
import bmesh


class MeshVolume(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_MeshVolume"
    bl_label = "Mesh Volume"

    bl_category = "Practical 1"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        # TODO: Check that the user has selected a mesh
        if context.active_object is None:
            self.layout.label(text='Select a mesh')
            return 

        # TODO: Obtain a BMesh from the selected mesh
        bm = bmesh.new()
        bm.from_mesh(context.active_object.data)


        # TODO: Apply the world transformation to the BMesh (so that scaling affects volume)
        bmesh.ops.transform(bm, matrix=context.active_object.matrix_world, verts=bm.verts)
        
        # TODO: Show the computed volume using a label
        self.layout.label(text=f'Volume: {mesh_volume(bm):.2f} cubic units')


