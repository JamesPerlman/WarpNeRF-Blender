import bpy
from typing import List

from warpnerf.scene.objects.blender_compatible import BlenderDeserializable
from warpnerf.scene.objects.dict_compatible import DictSerializable
from warpnerf.scene.objects.radiance_field import RadianceField
from warpnerf.scene.objects.scene_object import SceneObject, SceneObjectGroup
from warpnerf.utils.object_utilities import get_obj_type

interpretable_types = [RadianceField]
def interpret_obj(obj: bpy.types.Object):
    otype = get_obj_type(obj)

    for t in interpretable_types:
        if t.type() == otype:
            return t.from_blender(obj)

    return None

class WNScene(BlenderDeserializable, DictSerializable):
    objects: List[SceneObject]

    @classmethod
    def from_blender(cls, ctx, obj = None):
        scene = WNScene()
        scene.objects = []

        def traverse(obj: bpy.types.Object):
            if len(obj.children) > 0:
                for child in obj.children:
                    traverse(child)
            else:
                scene_obj = interpret_obj(obj)
                if scene_obj is not None:
                    scene.objects.append(scene_obj)

        for obj in ctx.scene.objects:
            traverse(obj)
        
        return scene
                

    def to_dict(self):
        return {
            "objects": [obj.to_dict() for obj in self.objects]
        }
