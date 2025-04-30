from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SfntTableReader(Protocol):
    @abstractmethod
    def get_or_parse_table(self, tag: str) -> 'SfntTable':
        raise NotImplementedError()


@runtime_checkable
class SfntTable(Protocol):
    @staticmethod
    @abstractmethod
    def parse(data: bytes, reader: SfntTableReader) -> 'SfntTable':
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> 'SfntTable':
        raise NotImplementedError()

    @abstractmethod
    def dump(self) -> bytes:
        raise NotImplementedError()
