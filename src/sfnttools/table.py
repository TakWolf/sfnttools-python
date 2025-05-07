from abc import abstractmethod
from typing import Protocol, runtime_checkable


@runtime_checkable
class SfntTableReader(Protocol):
    @abstractmethod
    def get_or_parse_table(self, tag: str) -> 'SfntTable':
        raise NotImplementedError()


@runtime_checkable
class SfntTableWriter(Protocol):
    @abstractmethod
    def get_table(self, tag: str, readonly: bool = True) -> 'SfntTable':
        raise NotImplementedError()

    @abstractmethod
    def replace_table(self, tag: str, table: 'SfntTable'):
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
    def dump(self, writer: SfntTableWriter) -> bytes:
        raise NotImplementedError()
