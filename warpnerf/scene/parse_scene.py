import bpy

from warpnerf.scene.object_utilities import is_warpnerf_obj

def parse_obj(obj: bpy.types.Object) -> dict:
    parseable_obj_types = 

def parse_scene(context: bpy.types.Context, scene: bpy.types.Scene) -> dict:
    wn_objs = [parse_obj(obj) for obj in scene.objects if is_warpnerf_obj(obj)]
