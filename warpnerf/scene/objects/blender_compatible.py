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

class BlenderUpdatable(ABC):
    @abstractmethod
    def update_from_blender(self, ctx: bpy.types.Context, obj: bpy.types.Object):
        pass

    @abstractmethod
    def update_to_blender(self, ctx: bpy.types.Context, obj: bpy.types.Object):
        pass

class BlenderCompatible(BlenderSerializable, BlenderDeserializable, BlenderUpdatable):
    pass
