from __future__ import annotations

from abc import abstractmethod
from typing import Any, Final, Protocol, runtime_checkable

from sfnttools.utils.stream import Stream


@runtime_checkable
class SignatureBlock(Protocol):
    @staticmethod
    @abstractmethod
    def parse(data: bytes) -> SignatureBlock:
        raise NotImplementedError()

    @property
    @abstractmethod
    def format(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> SignatureBlock:
        raise NotImplementedError()

    @abstractmethod
    def dump(self) -> bytes:
        raise NotImplementedError()


class SignatureBlockFormat1(SignatureBlock):
    @staticmethod
    def parse(data: bytes) -> SignatureBlockFormat1:
        stream = Stream(data)

        stream.read_uint16()
        stream.read_uint16()
        signature_length = stream.read_uint32()
        signature = stream.read(signature_length)

        return SignatureBlockFormat1(signature)

    signature: bytes

    def __init__(self, signature: bytes):
        self.signature = signature

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SignatureBlockFormat1):
            return False
        return self.signature == other.signature

    @property
    def format(self) -> int:
        return 1

    def copy(self) -> SignatureBlockFormat1:
        return SignatureBlockFormat1(self.signature)

    def dump(self) -> bytes:
        stream = Stream()

        stream.write_uint16(0)
        stream.write_uint16(0)
        stream.write_uint32(len(self.signature))
        stream.write(self.signature)

        return stream.get_value()


SIGNATURE_BLOCK_TYPE_REGISTRY: Final = {
    1: SignatureBlockFormat1,
}
