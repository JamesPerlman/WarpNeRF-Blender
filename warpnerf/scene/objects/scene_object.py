from abc import ABC, abstractmethod
from typing import List, Union

SceneObjectGroup = Union['SceneObject', List['SceneObjectGroup']]

class SceneObject(ABC):

    @abstractmethod
    @staticmethod
    def type(cls) -> str:
        pass
