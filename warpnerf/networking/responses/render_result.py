import bpy
import numpy as np
from dataclasses import dataclass
from io import BytesIO
from warpnerf.libs.imageio import imageio
from warpnerf.scene.objects.dict_compatible import DictDeserializable

class RenderResult(DictDeserializable):
    request_id: int
    pixels: np.ndarray

    @classmethod
    def from_dict(cls, data: dict) -> 'RenderResult':
        req = cls()
        req.request_id = data["request_id"]

        # Decode image using imageio
        image_array = imageio.imread(BytesIO(data["image"]), format='png')

        # Get dimensions and channels
        height, width, channels = image_array.shape

        # Ensure 4 channels (RGBA)
        if channels == 3:
            alpha = np.full((height, width, 1), 255, dtype=np.uint8)
            image_array = np.concatenate((image_array, alpha), axis=-1)

        # Normalize to Blender's format
        req.pixels = image_array.flatten().astype(np.float32) / 255.0



