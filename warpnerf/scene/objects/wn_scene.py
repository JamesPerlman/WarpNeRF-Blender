import bpy
from typing import List

from warpnerf.scene.objects.blender_compatible import BlenderDeserializable
from warpnerf.scene.objects.dict_compatible import DictSerializable
from warpnerf.scene.objects.radiance_field import RadianceField
from warpnerf.utils.object_utilities import get_obj_type

from typing import Union, get_args

SceneObject = Union[RadianceField]

def obj_from_blender(obj: bpy.types.Object) -> SceneObject:
    otype = get_obj_type(obj)

    for t in get_args(SceneObject):
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
                scene_obj = obj_from_blender(obj)
                if scene_obj is not None:
                    scene.objects.append(scene_obj)

        for obj in ctx.scene.objects:
            traverse(obj)
        
        return scene

    def to_dict(self):
        return {
            "objects": [obj.to_dict() for obj in self.objects]
        }
