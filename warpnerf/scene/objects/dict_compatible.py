from abc import ABC, abstractmethod

class DictSerializable(ABC):

    @abstractmethod
    def to_dict(self) -> dict:
        pass

class DictDeserializable(ABC):
    @abstractmethod
    @classmethod
    def from_dict(cls, data: dict):
        pass

class DictCompatible(DictSerializable, DictDeserializable):
    pass
