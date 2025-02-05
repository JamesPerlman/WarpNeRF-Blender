from typing import Tuple
import bpy
import numpy as np

from warpnerf.blender_utils.cameras import bl2wn_camera_focal_length, wn2bl_camera_focal_length
from warpnerf.scene.object_identifiers import WN_OTYPE_PERSPECTIVE_CAMERA
from warpnerf.scene.objects.dict_compatible import DictCompatible
from warpnerf.utils.object_utilities import set_obj_type
from warpnerf.scene.objects.blender_compatible import BlenderCompatible

class PerspectiveCamera(BlenderCompatible, DictCompatible):

    focal_length: float
    image_dims: Tuple[int, int]
    sensor_dims: Tuple[float, float]
    rotation_matrix: np.ndarray[Tuple[3, 3], np.float32]
    translation_vector: np.ndarray[Tuple[3], np.float32]
    
    @staticmethod
    def type(cls) -> str:
        return WN_OTYPE_PERSPECTIVE_CAMERA
    
    # DictSerializable methods
    def to_dict(self) -> dict:
        return {
            'f': self.focal_length,
            'img_w': self.image_dims[0],
            'img_h': self.image_dims[1],
            'sx': self.sensor_dims[0],
            'sy': self.sensor_dims[1],
            'R': self.rotation_matrix.tolist(),
            't': self.translation_vector.tolist(),
        }

    @classmethod
    def from_dict(cls, data: dict):
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
    def from_blender(
        cls,
        ctx: bpy.types.Context,
        obj: bpy.types.Object | bpy.types.RegionView3D
    ) -> 'PerspectiveCamera':
        cam = PerspectiveCamera()
        
        cam.update_from_blender(ctx, obj)
        
        return cam
    
    def update_from_blender(
        self,
        ctx: bpy.types.Context,
        obj: bpy.types.Object | bpy.types.RegionView3D
    ):
        if isinstance(obj, bpy.types.Object):
            self.focal_length = bl2wn_camera_focal_length(obj.data, self.image_dims)
            self.rotation_matrix = obj.matrix_world[:, :3]
            self.translation_vector = obj.matrix_world[:, 3]
            self.image_dims = (ctx.scene.render.resolution_x, ctx.scene.render.resolution_y)
            aspect_ratio = ctx.scene.render.resolution_y / ctx.scene.render.resolution_x
            self.sensor_dims = (1.0, aspect_ratio)
        
        elif isinstance(obj, bpy.types.RegionView3D):
            rv3d: bpy.types.RegionView3D = obj
            projection_matrix = np.array(rv3d.window_matrix)
            view_matrix = np.array(rv3d.view_matrix.inverted())
            self.focal_length = 0.5 * ctx.region.width * projection_matrix[0, 0]
            self.rotation_matrix = view_matrix[:3, :3]
            self.translation_vector = view_matrix[:3, 3]
            self.image_dims = (ctx.region.width, ctx.region.height)
            aspect_ratio = ctx.region.height / ctx.region.width
            self.sensor_dims = (1.0, aspect_ratio)
    
    def update_to_blender(self, ctx: bpy.types.Context, obj: bpy.types.Object):
        obj.matrix_world = np.concatenate([self.rotation_matrix, self.translation_vector], axis=1)
        obj.data.lens = wn2bl_camera_focal_length(obj.data, self.image_dims, self.focal_length)

    # equality operator
    def __eq__(self, other: 'PerspectiveCamera') -> bool:
        return (
            isinstance(other, PerspectiveCamera)
            and self.focal_length == other.focal_length
            and self.image_dims == other.image_dims
            and self.sensor_dims == other.sensor_dims
            and np.array_equal(self.rotation_matrix, other.rotation_matrix)
            and np.array_equal(self.translation_vector, other.translation_vector)
        )
