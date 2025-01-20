from abc import ABC, abstractmethod
from typing import List, Union

SceneObjectGroup = Union['SceneObject', List['SceneObjectGroup']]

from abc import ABC, abstractmethod

class SceneObject(ABC):
    def __init__(self):
        self._children = []

    @classmethod
    @abstractmethod
    def type(self) -> str:
        pass

    @property
    def children(self):
        return self._children

    def add_child(self, child):
        if isinstance(child, SceneObject):
            self._children.append(child)
        else:
            raise ValueError("Child must be an instance of SceneObject.")

    def __repr__(self):
        return f"<{self.type} with {len(self.children)} children>"
