import bpy
import inspect

from .genus import *
from .boundaries import *
from .volume import *
from .components import *
from .registration import *

bl_info = {
    "name": "GDP Practical Assignment 1",
    "author": "Add your names here!",
    "description": "A student implementation of Geometric Data Processing practical assignment 1.",
    "blender": (4, 0, 2),
    "version": (0, 0, 1),
    "location": "View3D",
    "warning": "",
    "category": "Mesh"
}

classes = [
    MeshBoundaryLoops,
    MeshGenus,
    MeshVolume,
    MeshConnectedComponents,
    ObjectICPRegistration
]


def register():
    for c in classes:
        try:
            bpy.utils.register_class(c)
        except AttributeError as e:
            print(
                f"Encountered an error while loading your {c.__name__} module, maybe you're missing some boilerplate?\n"
                f"\tError: '{e}'\n"
                f"\t(Take a look in '{inspect.getfile(c)}' to find out what's missing)"
            )

    bpy.types.VIEW3D_MT_object.append(ObjectICPRegistration.menu_func)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
