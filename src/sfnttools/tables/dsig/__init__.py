from abc import abstractmethod
from io import BytesIO
from typing import Final, Protocol, runtime_checkable

from sfnttools.error import SfntError
from sfnttools.flags import SfntFlags
from sfnttools.table import SfntTableReader, SfntTableWriter, SfntTable
from sfnttools.tables.dsig.headers import SignatureRecord
from sfnttools.utils.stream import Stream

DSIG_PERMISSION_FLAGS_MASK_CANNOT_BE_RESIGNED: Final = 0b_0000_0000_0000_0001


class DsigPermissionFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'DsigPermissionFlags':
        cannot_be_resigned = value & DSIG_PERMISSION_FLAGS_MASK_CANNOT_BE_RESIGNED > 0
        return DsigPermissionFlags(cannot_be_resigned)

    cannot_be_resigned: bool

    def __init__(self, cannot_be_resigned: bool = False):
        self.cannot_be_resigned = cannot_be_resigned

    @property
    def value(self) -> int:
        value = 0
        if self.cannot_be_resigned:
            value |= DSIG_PERMISSION_FLAGS_MASK_CANNOT_BE_RESIGNED
        return value

    def copy(self) -> 'DsigPermissionFlags':
        return DsigPermissionFlags(self.cannot_be_resigned)


@runtime_checkable
class SignatureBlock(Protocol):
    @staticmethod
    @abstractmethod
    def parse(data: bytes) -> 'SignatureBlock':
        raise NotImplementedError()

    @property
    @abstractmethod
    def format(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def copy(self) -> 'SignatureBlock':
        raise NotImplementedError()

    @abstractmethod
    def dump(self) -> bytes:
        raise NotImplementedError()


class SignatureBlockFormat1(SignatureBlock):
    @staticmethod
    def parse(data: bytes) -> 'SignatureBlockFormat1':
        stream = Stream(data)

        stream.read_uint16()
        stream.read_uint16()
        signature_length = stream.read_uint32()
        signature = stream.read(signature_length)

        return SignatureBlockFormat1(signature)

    signature: bytes

    def __init__(self, signature: bytes):
        self.signature = signature

    @property
    def format(self) -> int:
        return 1

    def copy(self) -> 'SignatureBlockFormat1':
        return SignatureBlockFormat1(self.signature)

    def dump(self) -> bytes:
        buffer = BytesIO()
        stream = Stream(buffer)

        stream.write_uint16(0)
        stream.write_uint16(0)
        stream.write_uint32(len(self.signature))
        stream.write(self.signature)

        return buffer.getvalue()


SIGNATURE_BLOCK_TYPE_REGISTRY: Final = {
    1: SignatureBlockFormat1,
}


class DsigTable(SfntTable):
    @staticmethod
    def parse(data: bytes, reader: SfntTableReader | None = None) -> 'DsigTable':
        stream = Stream(data)

        version = stream.read_uint32()
        num_signatures = stream.read_uint16()
        flags = DsigPermissionFlags.parse(stream.read_uint16())
        signature_blocks = []
        signature_records = [SignatureRecord.parse(stream) for _ in range(num_signatures)]
        for signature_record in signature_records:
            signature_block_type = SIGNATURE_BLOCK_TYPE_REGISTRY.get(signature_record.format, None)
            if signature_block_type is None:
                raise SfntError(f'[DSIG] unsupported signature format: {signature_record.format}')
            signature_block = signature_block_type.parse(signature_record.read_signature_block_data(stream))
            signature_blocks.append(signature_block)

        return DsigTable(
            version,
            flags,
            signature_blocks,
        )

    version: int
    flags: DsigPermissionFlags
    signature_blocks: list[SignatureBlock]

    def __init__(
            self,
            version: int = 1,
            flags: DsigPermissionFlags | None = None,
            signature_blocks: list[SignatureBlock] | None = None,
    ):
        self.version = version
        self.flags = DsigPermissionFlags() if flags is None else flags
        self.signature_blocks = [] if signature_blocks is None else signature_blocks

    @property
    def num_signatures(self) -> int:
        return len(self.signature_blocks)

    def copy(self) -> 'DsigTable':
        return DsigTable(
            self.version,
            self.flags.copy(),
            [signature_block.copy() for signature_block in self.signature_blocks],
        )

    def dump(self, writer: SfntTableWriter) -> bytes:
        buffer = BytesIO()
        stream = Stream(buffer)

        stream.seek(4 + 2 + 2 + (4 + 4 + 4) * self.num_signatures)
        signature_records = []
        for signature_block in self.signature_blocks:
            offset = stream.tell()
            length = stream.write(signature_block.dump())
            signature_records.append(SignatureRecord(
                signature_block.format,
                length,
                offset,
            ))

        stream.seek(0)
        stream.write_uint32(self.version)
        stream.write_uint16(self.num_signatures)
        stream.write_uint16(self.flags.value)
        for signature_record in signature_records:
            signature_record.dump(stream)

        return buffer.getvalue()
