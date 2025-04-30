from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SfntTableContainer(Protocol):
    @abstractmethod
    def get_table(self, tag: str) -> 'SfntTable':
        raise NotImplementedError()


@runtime_checkable
class SfntTable(Protocol):
    @staticmethod
    @abstractmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'SfntTable':
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> 'SfntTable':
        raise NotImplementedError()

    @abstractmethod
    def dump(self, container: SfntTableContainer) -> bytes:
        raise NotImplementedError()
