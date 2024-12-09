from abc import ABC, abstractmethod
class SceneObject(ABC):

    @abstractmethod
    @staticmethod
    def type(cls) -> str:
        pass
