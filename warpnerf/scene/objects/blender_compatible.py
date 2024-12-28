from typing import Any
import bpy
from abc import ABC, abstractmethod

class BlenderSerializable(ABC):

    @abstractmethod
    def to_blender(self) -> bpy.types.Object:
        pass

class BlenderDeserializable(ABC):
    @abstractmethod
    @classmethod
    def from_blender(cls, ctx: bpy.types.Context, obj: Any):
        pass

class BlenderCompatible(BlenderSerializable, BlenderDeserializable):
    pass
