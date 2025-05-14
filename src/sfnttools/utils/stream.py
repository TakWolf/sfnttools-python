import os
from io import BytesIO, StringIO
from typing import BinaryIO

from sfnttools.utils.math import round_half_up


class Stream:
    source: BinaryIO

    def __init__(self, source: bytes | bytearray | BinaryIO | None = None):
        if source is None:
            source = BytesIO()
        elif isinstance(source, (bytes, bytearray)):
            source = BytesIO(source)
        self.source = source

    def read(self, size: int, ignore_eof: bool = False) -> bytes:
        values = self.source.read(size)
        if len(values) < size and not ignore_eof:
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
        major_version = self.read_uint16()
        minor_version = self.read_uint16() >> 12
        return major_version, minor_version

    def read_255uint16(self) -> int:
        code = self.read_uint8()
        if code == 253:
            value = self.read_uint8()
            value <<= 8
            value &= 0xFF00
            value |= self.read_uint8() & 0x00FF
        elif code == 254:
            value = self.read_uint8()
            value += 506
        elif code == 255:
            value = self.read_uint8()
            value += 253
        else:
            value = code
        return value

    def read_uint_base128(self) -> int:
        value = 0
        for i in range(5):
            code = self.read_uint8()
            if i == 0 and code == 0x80:
                raise ValueError('uint_base128 bytes must not start with leading zeros')
            value <<= 7
            value |= code & 0x7F
            if value >= 2 ** 32:
                raise ValueError('uint_base128 value exceeds 2 ** 32 - 1')
            if code & 0x80 == 0:
                return value
        raise ValueError('uint_base128 sequence exceeds 5 bytes')

    def read_binary_string(self, size: int) -> str:
        value = StringIO()
        for b in self.read(size):
            value.write(f'{b:08b}')
        return value.getvalue()

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
        return self.write_int32(round_half_up(value * (2 ** 16)))

    def write_fword(self, value: int) -> int:
        return self.write_int16(value)

    def write_ufword(self, value: int) -> int:
        return self.write_uint16(value)

    def write_f2dot14(self, value: float) -> int:
        return self.write_int16(round_half_up(value * (2 ** 14)))

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
        major_version, minor_version = value
        if not 0 <= minor_version <= 9:
            raise ValueError('minor version requires 0 <= integer <= 9')

        minor_version <<= 12
        return self.write_uint16(major_version) + self.write_uint16(minor_version)

    def write_255uint16(self, value: int) -> int:
        if not 0 <= value <= 0xFFFF:
            raise ValueError('255uint16 requires 0 <= integer <= 65535')

        if value < 253:
            return self.write_uint8(value)
        elif value < 506:
            return self.write_uint8(255) + self.write_uint8(value - 253)
        elif value < 762:
            return self.write_uint8(254) + self.write_uint8(value - 506)
        else:
            return self.write_uint8(253) + self.write_uint8((value >> 8) & 0xFF) + self.write_uint8(value & 0xFF)

    def write_uint_base128(self, value: int) -> int:
        if not 0 <= value < 2 ** 32:
            raise ValueError('uint_base128 requires 0 <= integer < 2 ** 32')

        buffer = bytearray()
        while True:
            buffer.append(value & 0x7F)
            value >>= 7
            if value == 0:
                break

        size = 0
        for i, code in enumerate(reversed(buffer)):
            if i != len(buffer) - 1:
                code |= 0x80
            size += self.write_uint8(code)
        return size

    def write_binary_string(self, value: str) -> int:
        if len(value) % 8 != 0:
            raise ValueError('the length must be a multiple of 8')

        return self.write(bytes(int(value[i:i + 8], 2) for i in range(0, len(value), 8)))

    def write_nulls(self, size: int) -> int:
        for _ in range(size):
            self.write(b'\x00')
        return size

    def align_to_2_byte_with_nulls(self) -> int:
        return self.write_nulls(1 - (self.tell() + 1) % 2)

    def align_to_4_byte_with_nulls(self) -> int:
        return self.write_nulls(3 - (self.tell() + 3) % 4)

    def seek(self, offset: int, whence: int = os.SEEK_SET):
        self.source.seek(offset, whence)

    def tell(self) -> int:
        return self.source.tell()

    def get_value(self) -> bytes:
        if not isinstance(self.source, BytesIO):
            raise ValueError("non 'BytesIO' source cannot get value")
        return self.source.getvalue()
