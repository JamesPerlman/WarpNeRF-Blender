import bpy
from abc import ABC, abstractmethod

class BlenderCompatible(ABC):

    @abstractmethod
    def to_blender(self) -> bpy.types.Object:
        pass
    
    @abstractmethod
    @classmethod
    def from_blender(cls, ctx: bpy.types.Context, obj: bpy.types.Object):
        pass
