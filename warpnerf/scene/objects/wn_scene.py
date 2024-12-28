import bpy
from typing import List

from warpnerf.scene.objects.blender_compatible import BlenderDeserializable
from warpnerf.scene.objects.dict_compatible import DictSerializable
from warpnerf.scene.objects.perspective_camera import PerspectiveCamera
from warpnerf.scene.objects.scene_object import SceneObject, SceneObjectGroup

class WNScene(BlenderDeserializable, DictSerializable):
    camera: PerspectiveCamera
    objects: SceneObjectGroup

    @classmethod
    def from_blender(cls, ctx, obj = None):
        scene = WNScene()
        scene.camera = PerspectiveCamera.from_blender(ctx, ctx.scene.camera)
        scene.objects = []
        for obj in ctx.scene.objects:
            if obj.parent is None:
                scene.objects.append(SceneObject.from_blender(ctx, obj))
            else:
                

    def to_dict(self):
        return super().to_dict()