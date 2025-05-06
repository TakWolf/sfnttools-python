from abc import abstractmethod
from typing import Protocol, runtime_checkable

from sfnttools.utils.stream import Stream


@runtime_checkable
class GlyphDescription(Protocol):
    @staticmethod
    @abstractmethod
    def parse(stream: Stream) -> 'GlyphDescription':
        raise NotImplementedError()

    x_min: int
    y_min: int
    x_max: int
    y_max: int

    @abstractmethod
    def copy(self) -> 'GlyphDescription':
        raise NotImplementedError()

    @abstractmethod
    def dump(self) -> bytes:
        raise NotImplementedError()
