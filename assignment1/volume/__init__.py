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

        # TODO: Obtain a BMesh from the selected mesh

        # TODO: Apply the world transformation to the BMesh (so that scaling affects volume)

        # TODO: Show the computed volume using a label

        pass



