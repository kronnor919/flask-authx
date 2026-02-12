from abc import ABC, abstractmethod


class IPasswordHashing(ABC):
    @abstractmethod
    def hash(self, password: str) -> str:
        pass

    @abstractmethod
    def verify(self, password: str, hashed: str) -> bool:
        pass
