from abc import ABC, abstractmethod
from typing import List, Union

SceneObjectGroup = Union['SceneObject', List['SceneObjectGroup']]

class SceneObject(ABC):

    @staticmethod
    @abstractmethod
    def type(cls) -> str:
        pass
