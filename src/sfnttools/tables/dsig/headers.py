from __future__ import annotations

from sfnttools.utils.stream import Stream


class SignatureRecord:
    @staticmethod
    def parse(stream: Stream) -> SignatureRecord:
        format = stream.read_uint32()
        length = stream.read_uint32()
        offset = stream.read_offset32()
        return SignatureRecord(
            format,
            length,
            offset,
        )

    format: int
    length: int
    offset: int

    def __init__(
            self,
            format: int,
            length: int,
            offset: int,
    ):
        self.format = format
        self.length = length
        self.offset = offset

    def read_signature_block_data(self, stream: Stream) -> bytes:
        stream.seek(self.offset)
        data = stream.read(self.length)
        return data

    def dump(self, stream: Stream):
        stream.write_uint32(self.format)
        stream.write_uint32(self.length)
        stream.write_offset32(self.offset)
