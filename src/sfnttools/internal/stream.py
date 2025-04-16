from typing import BinaryIO


class Stream:
    source: BinaryIO

    def __init__(self, source: BinaryIO):
        self.source = source

    def read(self, size: int) -> bytes:
        values = self.source.read(size)
        if len(values) < size:
            raise EOFError()
        return values

    def read_uint8(self) -> int:
        return int.from_bytes(self.read(1), 'big', signed=False)

    def read_int8(self) -> int:
        return int.from_bytes(self.read(1), 'big', signed=True)

    def read_uint16(self) -> int:
        return int.from_bytes(self.read(2), 'big', signed=False)

    def read_int16(self) -> int:
        return int.from_bytes(self.read(2), 'big', signed=True)

    def read_uint24(self) -> int:
        return int.from_bytes(self.read(3), 'big', signed=False)

    def read_uint32(self) -> int:
        return int.from_bytes(self.read(4), 'big', signed=False)

    def read_int32(self) -> int:
        return int.from_bytes(self.read(4), 'big', signed=True)

    def read_fixed(self) -> float:
        return self.read_int32() / (2 ** 16)

    def read_fword(self) -> int:
        return self.read_int16()

    def read_ufword(self) -> int:
        return self.read_uint16()

    def read_f2dot14(self) -> float:
        return self.read_int16() / (2 ** 14)

    def read_long_datetime(self) -> int:
        return int.from_bytes(self.read(8), 'big', signed=True)

    def read_tag(self) -> str:
        return self.read(4).decode('latin-1')

    def read_offset8(self) -> int:
        return self.read_uint8()

    def read_offset16(self) -> int:
        return self.read_uint16()

    def read_offset24(self) -> int:
        return self.read_uint24()

    def read_offset32(self) -> int:
        return self.read_uint32()

    def read_version_16dot16(self) -> tuple[int, int]:
        return self.read_uint16(), self.read_uint16()

    def write(self, values: bytes) -> int:
        return self.source.write(values)

    def write_uint8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=False))

    def write_int8(self, value: int) -> int:
        return self.write(value.to_bytes(1, 'big', signed=True))

    def write_uint16(self, value: int) -> int:
        return self.write(value.to_bytes(2, 'big', signed=False))

    def write_int16(self, value: int) -> int:
        return self.write(value.to_bytes(2, 'big', signed=True))

    def write_uint24(self, value: int) -> int:
        return self.write(value.to_bytes(3, 'big', signed=False))

    def write_uint32(self, value: int) -> int:
        return self.write(value.to_bytes(4, 'big', signed=False))

    def write_int32(self, value: int) -> int:
        return self.write(value.to_bytes(4, 'big', signed=True))

    def write_fixed(self, value: float) -> int:
        return self.write_int32(int(value * (2 ** 16)))

    def write_fword(self, value: int) -> int:
        return self.write_int16(value)

    def write_ufword(self, value: int) -> int:
        return self.write_uint16(value)

    def write_f2dot14(self, value: float) -> int:
        return self.write_int16(int(value * (2 ** 14)))

    def write_long_datetime(self, value: int) -> int:
        return self.write(value.to_bytes(8, 'big', signed=True))

    def write_tag(self, value: str) -> int:
        data = value.encode('latin-1')
        if len(data) != 4:
            raise ValueError('bytes length must be 4')
        return self.write(data)

    def write_offset8(self, value: int) -> int:
        return self.write_uint8(value)

    def write_offset16(self, value: int) -> int:
        return self.write_uint16(value)

    def write_offset24(self, value: int) -> int:
        return self.write_uint24(value)

    def write_offset32(self, value: int) -> int:
        return self.write_uint32(value)

    def write_version_16dot16(self, value: tuple[int, int]) -> int:
        return self.write_uint16(value[0]) + self.write_uint16(value[1])

    def seek(self, offset: int):
        self.source.seek(offset)

    def tell(self) -> int:
        return self.source.tell()
