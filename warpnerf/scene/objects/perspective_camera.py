from typing import Tuple
import bpy
import numpy as np

from warpnerf.blender_utils.cameras import bl2wn_camera_focal_length, wn2bl_camera_focal_length
from warpnerf.scene.object_identifiers import OTYPE_TRAIN_CAM
from warpnerf.utils.object_utilities import set_obj_type
from warpnerf.scene.objects.blender_compatible import BlenderCompatible
from warpnerf.scene.objects.scene_object import SceneObject

class PerspectiveCamera(SceneObject, BlenderCompatible):

    focal_length: float
    image_dims: Tuple[int, int]
    sensor_dims: Tuple[float, float]
    rotation_matrix: np.ndarray[Tuple[3, 3], np.float32]
    translation_vector: np.ndarray[Tuple[3], np.float32]
    
    @staticmethod
    def type(cls) -> str:
        return 'warpnerf_otype_perspective_camera'
    
    # DictSerializable methods
    def serialize(self) -> dict:
        return {
            'f': self.focal_length,
            'img_w': self.image_dims[0],
            'img_h': self.image_dims[1],
            'sx': self.sensor_dims[0],
            'sy': self.sensor_dims[1],
            'R': self.rotation_matrix.tolist(),
            't': self.translation_vector.tolist()
        }

    @classmethod
    def deserialize(cls, data: dict):
        cam = PerspectiveCamera()
        cam.focal_length = data['f']
        cam.image_dims = (data['img_w'], data['img_h'])
        cam.sensor_dims = (data['sx'], data['sy'])
        cam.rotation_matrix = np.array(data['R'], dtype=np.float32)
        cam.translation_vector = np.array(data['t'], dtype=np.float32)
        
        return cam

    # BlenderCompatible methods
    def to_blender(self) -> bpy.types.Object:
        cam_data = bpy.types.Camera()
        cam_obj = bpy.types.Object()
        cam_obj.data = cam_data

        set_obj_type(cam_obj, self.__class__.type())

        self.update_to_blender(None, cam_obj)

        return cam_obj

    @classmethod
    def from_blender(cls, ctx: bpy.types.Context, obj: bpy.types.Object) -> 'PerspectiveCamera':
        cam = PerspectiveCamera()
        
        cam.update_from_blender(ctx, obj)
        
        return cam
    
    def update_from_blender(self, ctx: bpy.types.Context, obj: bpy.types.Object):
        self.focal_length = bl2wn_camera_focal_length(obj.data, self.image_dims)
        self.rotation_matrix = obj.matrix_world[:, :3]
        self.translation_vector = obj.matrix_world[:, 3]
        self.image_dims = (ctx.scene.render.resolution_x, ctx.scene.render.resolution_y)
        aspect_ratio = ctx.scene.render.resolution_y / ctx.scene.render.resolution_x
        self.sensor_dims = (1.0, aspect_ratio)
    
    def update_to_blender(self, ctx: bpy.types.Context, obj: bpy.types.Object):
        obj.matrix_world = np.concatenate([self.rotation_matrix, self.translation_vector], axis=1)
        obj.data.lens = wn2bl_camera_focal_length(obj.data, self.image_dims, self.focal_length)
