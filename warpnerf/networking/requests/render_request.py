from typing import Any, Tuple

from warpnerf.scene.objects.dict_compatible import DictSerializable
from warpnerf.scene.objects.perspective_camera import PerspectiveCamera
from warpnerf.scene.objects.wn_scene import WNScene

class RenderRequest(DictSerializable):
    id: any
    scene: WNScene
    camera: PerspectiveCamera
    size: Tuple[int, int]

    def to_dict(self):
        return {
            "id": self.id,
            "scene": self.scene.to_dict(),
            "camera": self.camera.to_dict(),
            "size": self.size
        }
