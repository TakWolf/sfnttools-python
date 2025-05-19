from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.error import SfntError
from sfnttools.table import SfntTable
from sfnttools.tables.dsig.blocks import SignatureBlock, SIGNATURE_BLOCK_TYPE_REGISTRY
from sfnttools.tables.dsig.flags import DsigPermissionFlags
from sfnttools.tables.dsig.headers import SignatureRecord
from sfnttools.utils.stream import Stream


class DsigTable(SfntTable):
    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> DsigTable:
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

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DsigTable):
            return False
        return (self.version == other.version and
                self.flags == other.flags and
                self.signature_blocks == other.signature_blocks)

    @property
    def num_signatures(self) -> int:
        return len(self.signature_blocks)

    def copy(self) -> DsigTable:
        signature_blocks = [signature_block.copy() for signature_block in self.signature_blocks]
        return DsigTable(
            self.version,
            self.flags.copy(),
            signature_blocks,
        )

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        stream = Stream()

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

        return stream.get_value()
