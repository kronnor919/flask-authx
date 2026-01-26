from abc import ABC, abstractmethod


class IDatabaseSetup(ABC):
    @abstractmethod
    def init(self) -> None:
        pass
