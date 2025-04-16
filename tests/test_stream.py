import random
from io import BytesIO

import pytest

from sfnttools.internal.stream import Stream


def test_byte():
    stream = Stream(BytesIO())
    size = stream.write(b'Hello World')
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read(11) == b'Hello World'
    assert stream.tell() == size


def test_eof():
    stream = Stream(BytesIO())
    with pytest.raises(EOFError):
        stream.read(1)


def test_uint8():
    values = [random.randint(0, 0xFF) for _ in range(20)]

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_long_datetime(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_long_datetime() == value
    assert stream.tell() == size


def test_tag():
    stream = Stream(BytesIO())
    size = stream.write_tag('head')
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_tag() == 'head'
    assert stream.tell() == size


def test_offset8():
    values = [random.randint(0, 0xFF) for _ in range(20)]

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
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

    stream = Stream(BytesIO())
    size = 0
    for value in values:
        size += stream.write_offset32(value)
    assert stream.tell() == size
    stream.seek(0)
    for value in values:
        assert stream.read_offset32() == value
    assert stream.tell() == size


def test_version_16dot16():
    stream = Stream(BytesIO())
    size = stream.write_version_16dot16((1, 2))
    assert stream.tell() == size
    stream.seek(0)
    assert stream.read_version_16dot16() == (1, 2)
    assert stream.tell() == size
