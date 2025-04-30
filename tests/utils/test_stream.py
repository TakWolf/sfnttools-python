import random

import pytest

from sfnttools.utils.stream import Stream


def test_byte():
    stream = Stream()
    size = stream.write(b'Hello World')
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read(11) == b'Hello World'
    assert stream.tell() == size


def test_eof():
    stream = Stream()
    with pytest.raises(EOFError):
        stream.read(1)


def test_uint8():
    values = [random.randint(0, 0xFF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_uint8(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint8() == value
    assert stream.tell() == size


def test_int8():
    values = [random.randint(-0x80, 0x7F) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_int8(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int8() == value
    assert stream.tell() == size


def test_uint16():
    values = [random.randint(0, 0xFF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_uint16(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint16() == value
    assert stream.tell() == size


def test_int16():
    values = [random.randint(-0x80_00, 0x7F_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_int16(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int16() == value
    assert stream.tell() == size


def test_uint24():
    values = [random.randint(0, 0xFF_FF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_uint24(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint24() == value
    assert stream.tell() == size


def test_uint32():
    values = [random.randint(0, 0xFF_FF_FF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_uint32(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_uint32() == value
    assert stream.tell() == size


def test_int32():
    values = [random.randint(-0x80_00_00_00, 0x7F_FF_FF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_int32(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_int32() == value
    assert stream.tell() == size


def test_fixed():
    values = [random.randint(-0x80_00, 0x7F_FF) / (2 ** 16) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_fixed(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_fixed() == value
    assert stream.tell() == size


def test_fword():
    values = [random.randint(-0x80_00, 0x7F_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_fword(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_fword() == value
    assert stream.tell() == size


def test_ufword():
    values = [random.randint(0, 0xFF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_ufword(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_ufword() == value
    assert stream.tell() == size


def test_f2dot14():
    values = [random.randint(-0x80_00, 0x7F_FF) / (2 ** 14) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_f2dot14(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_f2dot14() == value
    assert stream.tell() == size


def test_long_datetime():
    values = [random.randint(-0x80_00_00_00_00_00_00_00, 0x7F_FF_FF_FF_FF_FF_FF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_long_datetime(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_long_datetime() == value
    assert stream.tell() == size


def test_tag():
    stream = Stream()
    size = stream.write_tag('head')
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_tag() == 'head'
    assert stream.tell() == size


def test_offset8():
    values = [random.randint(0, 0xFF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_offset8(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_offset8() == value
    assert stream.tell() == size


def test_offset16():
    values = [random.randint(0, 0xFF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_offset16(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_offset16() == value
    assert stream.tell() == size


def test_offset24():
    values = [random.randint(0, 0xFF_FF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_offset24(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_offset24() == value
    assert stream.tell() == size


def test_offset32():
    values = [random.randint(0, 0xFF_FF_FF_FF) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_offset32(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_offset32() == value
    assert stream.tell() == size


def test_version_16dot16():
    values = [random.randint(0, 0xFF_FF_FF_FF) / (2 ** 16) for _ in range(20)]

    stream = Stream()
    size = 0
    for value in values:
        size += stream.write_version_16dot16(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_version_16dot16() == value
    assert stream.tell() == size


def test_255uint16():
    stream = Stream()
    assert stream.write_255uint16(252) == 1
    assert stream.write_255uint16(506) == 2
    assert stream.write_255uint16(762) == 3
    assert stream.write(b'\xfc') == 1
    assert stream.write(b'\xfe\x00') == 2
    assert stream.write(b'\xff\xfd') == 2
    assert stream.write(b'\xfd\x01\xfa') == 3
    assert stream.write(b'\xfd\x02\xfa') == 3
    stream.seek(0)
    assert stream.read(1) == b'\xfc'
    assert stream.read(2) == b'\xfe\x00'
    assert stream.read(3) == b'\xfd\x02\xfa'
    assert stream.read_255uint16() == 252
    assert stream.read_255uint16() == 506
    assert stream.read_255uint16() == 506
    assert stream.read_255uint16() == 506
    assert stream.read_255uint16() == 762


def test_uint_base128():
    stream = Stream()
    assert stream.write_uint_base128(63) == 1
    assert stream.write_uint_base128(2 ** 32 - 1) == 5
    assert stream.write(b'\x3f') == 1
    assert stream.write(b'\x8f\xff\xff\xff\x7f') == 5
    stream.seek(0)
    assert stream.read(1) == b'\x3f'
    assert stream.read(5) == b'\x8f\xff\xff\xff\x7f'
    assert stream.read_uint_base128() == 63
    assert stream.read_uint_base128() == 2 ** 32 - 1


def test_align_to_4_byte():
    stream = Stream()
    stream.write(b'abc')
    assert stream.align_to_4_byte_with_nulls() == 1
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read(4) == b'abc\x00'
