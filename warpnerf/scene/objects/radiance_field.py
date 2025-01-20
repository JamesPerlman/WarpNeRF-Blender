import bpy
import mathutils
import numpy as np

from typing import Tuple
from warpnerf.scene.objects.blender_compatible import BlenderCompatible
from warpnerf.scene.objects.dict_compatible import DictCompatible
from warpnerf.scene.objects.scene_object import SceneObject
from warpnerf.utils.object_utilities import get_obj_attr, get_obj_id, set_obj_attr, set_obj_id

class RadianceField(SceneObject, DictCompatible, BlenderCompatible):
    
    id: int = 0
    rf_type: str = 'nerf'
    bbox_size: float = 1.0
    transform: np.ndarray[Tuple[4, 4], np.float32] = np.eye(4, dtype=np.float32)
    is_trainable: bool = True
    is_training_enabled: bool = False
    limit_training: bool = True
    n_steps_max: int = 10000
    n_steps_trained: int = 0
    n_images_loaded: int = 0
    n_images_total: int = 0

    @classmethod
    def type(cls) -> str:
        return 'warpnerf_otype_radiance_field'
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'rf_type': self.rf_type,
            'bbox_size': self.bbox_size,
            'transform': self.transform.tolist(),
            'is_trainable': self.is_trainable,
            'is_training_enabled': self.is_training_enabled,
            'limit_training': self.limit_training,
            'n_steps_max': self.n_steps_max,
            'n_steps_trained': self.n_steps_trained,
            'n_images_loaded': self.n_images_loaded,
            'n_images_total': self.n_images_total
        }

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()

        obj.id = data['id']
        obj.rf_type = data['rf_type']
        obj.bbox_size = data['bbox_size']
        obj.transform = np.array(data['transform'], dtype=np.float32)
        obj.is_trainable = data['is_trainable']
        obj.is_training_enabled = data['is_training_enabled']
        obj.limit_training = data['limit_training']
        obj.n_steps_max = data['n_steps_max']
        obj.n_steps_trained = data['n_steps_trained']
        obj.n_images_loaded = data['n_images_loaded']
        obj.n_images_total = data['n_images_total']

        return obj

    def to_blender(self) -> bpy.types.Object:
        obj = bpy.data.objects.new('Radiance Field Object', None)
        
        self.update_to_blender(None, obj)

        return obj
    
    def update_to_blender(self, ctx: bpy.types.Context, obj: bpy.types.Object):
        obj.matrix_world = mathutils.Matrix(self.transform)
        set_obj_id(obj, self.id)
        set_obj_attr(obj, 'rf_type', self.rf_type)
        set_obj_attr(obj, 'bbox_size', self.bbox_size)
        set_obj_attr(obj, 'is_trainable', self.is_trainable)
        set_obj_attr(obj, 'is_training_enabled', self.is_training_enabled)
        set_obj_attr(obj, 'limit_training', self.limit_training)
        set_obj_attr(obj, 'n_steps_max', self.n_steps_max)
        set_obj_attr(obj, 'n_steps_trained', self.n_steps_trained)
        set_obj_attr(obj, 'n_images_loaded', self.n_images_loaded)
        set_obj_attr(obj, 'n_images_total', self.n_images_total)
    
    @classmethod
    def from_blender(cls, obj: bpy.types.Object) -> 'RadianceField':
        rf = RadianceField()

        rf.update_from_blender(None, obj)

        return rf

    def update_from_blender(self, ctx: bpy.types.Context, obj: bpy.types.Object):
        self.id                     = get_obj_id(obj)
        self.transform              = np.array(obj.matrix_world, dtype=np.float32)
        self.rf_type                = get_obj_attr(obj, 'rf_type')
        self.bbox_size              = get_obj_attr(obj, 'bbox_size')
        self.is_trainable           = get_obj_attr(obj, 'is_trainable')
        self.is_training_enabled    = get_obj_attr(obj, 'is_training_enabled')
        self.limit_training         = get_obj_attr(obj, 'limit_training')
        self.n_steps_max            = get_obj_attr(obj, 'n_steps_max')
        self.n_steps_trained        = get_obj_attr(obj, 'n_steps_trained')
        self.n_images_loaded        = get_obj_attr(obj, 'n_images_loaded')
        self.n_images_total         = get_obj_attr(obj, 'n_images_total')
