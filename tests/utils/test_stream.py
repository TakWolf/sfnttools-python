import pytest

from sfnttools.utils.math import round_half_up
from sfnttools.utils.stream import Stream


def test_bytes():
    stream = Stream()
    assert stream.write(b'Hello World') == 11
    assert stream.tell() == 11
    stream.seek(0)
    assert stream.read(11) == b'Hello World'
    assert stream.tell() == 11


def test_eof():
    stream = Stream()
    stream.write(b'ABC')
    with pytest.raises(EOFError):
        stream.read(4)
    stream.seek(0)
    assert stream.read(4, ignore_eof=True) == b'ABC'


def test_uint8():
    stream = Stream()
    assert stream.write_uint8(0x00) == 1
    assert stream.write_uint8(0xFF) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_uint8() == 0x00
    assert stream.read_uint8() == 0xFF
    assert stream.tell() == 2


def test_int8():
    stream = Stream()
    assert stream.write_int8(-0x80) == 1
    assert stream.write_int8(0x7F) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_int8() == -0x80
    assert stream.read_int8() == 0x7F
    assert stream.tell() == 2


def test_uint16():
    stream = Stream()
    assert stream.write_uint16(0x0000) == 2
    assert stream.write_uint16(0xFFFF) == 2
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_uint16() == 0x0000
    assert stream.read_uint16() == 0xFFFF
    assert stream.tell() == 4


def test_int16():
    stream = Stream()
    assert stream.write_int16(-0x8000) == 2
    assert stream.write_int16(0x7FFF) == 2
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_int16() == -0x8000
    assert stream.read_int16() == 0x7FFF
    assert stream.tell() == 4


def test_uint24():
    stream = Stream()
    assert stream.write_uint24(0x000000) == 3
    assert stream.write_uint24(0xFFFFFF) == 3
    assert stream.tell() == 6
    stream.seek(0)
    assert stream.read_uint24() == 0x000000
    assert stream.read_uint24() == 0xFFFFFF
    assert stream.tell() == 6


def test_uint32():
    stream = Stream()
    assert stream.write_uint32(0x00000000) == 4
    assert stream.write_uint32(0xFFFFFFFF) == 4
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_uint32() == 0x00000000
    assert stream.read_uint32() == 0xFFFFFFFF
    assert stream.tell() == 8


def test_int32():
    stream = Stream()
    assert stream.write_int32(-0x80000000) == 4
    assert stream.write_int32(0x7FFFFFFF) == 4
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_int32() == -0x80000000
    assert stream.read_int32() == 0x7FFFFFFF
    assert stream.tell() == 8


def test_fixed():
    stream = Stream()
    assert stream.write_fixed(-0x8000 / (2 ** 16)) == 4
    assert stream.write_fixed(0x7FFF / (2 ** 16)) == 4
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_fixed() == -0x8000 / (2 ** 16)
    assert stream.read_fixed() == 0x7FFF / (2 ** 16)
    assert stream.tell() == 8


def test_fword():
    stream = Stream()
    assert stream.write_fword(-0x8000) == 2
    assert stream.write_fword(0x7FFF) == 2
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_fword() == -0x8000
    assert stream.read_fword() == 0x7FFF
    assert stream.tell() == 4


def test_ufword():
    stream = Stream()
    assert stream.write_ufword(0x0000) == 2
    assert stream.write_ufword(0xFFFF) == 2
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_ufword() == 0x0000
    assert stream.read_ufword() == 0xFFFF
    assert stream.tell() == 4


def test_f2dot14():
    stream = Stream()
    assert stream.write_f2dot14(1.999939) == 2
    assert stream.write_f2dot14(1.75) == 2
    assert stream.write_f2dot14(0.000061) == 2
    assert stream.write_f2dot14(0.0) == 2
    assert stream.write_f2dot14(-0.000061) == 2
    assert stream.write_f2dot14(-2.0) == 2
    assert stream.write_uint16(0x7FFF) == 2
    assert stream.write_uint16(0x7000) == 2
    assert stream.write_uint16(0x0001) == 2
    assert stream.write_uint16(0x0000) == 2
    assert stream.write_uint16(0xFFFF) == 2
    assert stream.write_uint16(0x8000) == 2
    assert stream.tell() == 24
    stream.seek(0)
    assert stream.read_uint16() == 0x7FFF
    assert stream.read_uint16() == 0x7000
    assert stream.read_uint16() == 0x0001
    assert stream.read_uint16() == 0x0000
    assert stream.read_uint16() == 0xFFFF
    assert stream.read_uint16() == 0x8000
    assert round_half_up(stream.read_f2dot14(), 6) == 1.999939
    assert stream.read_f2dot14() == 1.75
    assert round_half_up(stream.read_f2dot14(), 6) == 0.000061
    assert stream.read_f2dot14() == 0.0
    assert round_half_up(stream.read_f2dot14(), 6) == -0.000061
    assert stream.read_f2dot14() == -2.0
    assert stream.tell() == 24


def test_long_datetime():
    stream = Stream()
    assert stream.write_long_datetime(-0x8000000000000000) == 8
    assert stream.write_long_datetime(0x7FFFFFFFFFFFFFFF) == 8
    assert stream.tell() == 16
    stream.seek(0)
    assert stream.read_long_datetime() == -0x8000000000000000
    assert stream.read_long_datetime() == 0x7FFFFFFFFFFFFFFF
    assert stream.tell() == 16


def test_tag():
    stream = Stream()
    assert stream.write_tag('head') == 4
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_tag() == 'head'
    assert stream.tell() == 4


def test_offset8():
    stream = Stream()
    assert stream.write_offset8(0x00) == 1
    assert stream.write_offset8(0xFF) == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read_offset8() == 0x00
    assert stream.read_offset8() == 0xFF
    assert stream.tell() == 2


def test_offset16():
    stream = Stream()
    assert stream.write_offset16(0x0000) == 2
    assert stream.write_offset16(0xFFFF) == 2
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_offset16() == 0x0000
    assert stream.read_offset16() == 0xFFFF
    assert stream.tell() == 4


def test_offset24():
    stream = Stream()
    assert stream.write_offset24(0x000000) == 3
    assert stream.write_offset24(0xFFFFFF) == 3
    assert stream.tell() == 6
    stream.seek(0)
    assert stream.read_offset24() == 0
    assert stream.read_offset24() == 0xFFFFFF
    assert stream.tell() == 6


def test_offset32():
    stream = Stream()
    assert stream.write_offset32(0x00000000) == 4
    assert stream.write_offset32(0xFFFFFFFF) == 4
    assert stream.tell() == 8
    stream.seek(0)
    assert stream.read_offset32() == 0x00000000
    assert stream.read_offset32() == 0xFFFFFFFF
    assert stream.tell() == 8


def test_version_16dot16():
    stream = Stream()
    assert stream.write_version_16dot16((0, 5)) == 4
    assert stream.write_version_16dot16((1, 0)) == 4
    assert stream.write_version_16dot16((1, 1)) == 4
    assert stream.tell() == 12
    stream.seek(0)
    assert stream.read_version_16dot16() == (0, 5)
    assert stream.read_version_16dot16() == (1, 0)
    assert stream.read_version_16dot16() == (1, 1)
    assert stream.tell() == 12


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
    assert stream.tell() == 17
    stream.seek(0)
    assert stream.read(1) == b'\xfc'
    assert stream.read(2) == b'\xfe\x00'
    assert stream.read(3) == b'\xfd\x02\xfa'
    assert stream.read_255uint16() == 252
    assert stream.read_255uint16() == 506
    assert stream.read_255uint16() == 506
    assert stream.read_255uint16() == 506
    assert stream.read_255uint16() == 762
    assert stream.tell() == 17


def test_uint_base128():
    stream = Stream()
    assert stream.write_uint_base128(63) == 1
    assert stream.write_uint_base128(2 ** 32 - 1) == 5
    assert stream.write(b'\x3f') == 1
    assert stream.write(b'\x8f\xff\xff\xff\x7f') == 5
    assert stream.tell() == 12
    stream.seek(0)
    assert stream.read(1) == b'\x3f'
    assert stream.read(5) == b'\x8f\xff\xff\xff\x7f'
    assert stream.read_uint_base128() == 63
    assert stream.read_uint_base128() == 2 ** 32 - 1
    assert stream.tell() == 12


def test_binary_string():
    stream = Stream()
    assert stream.write_binary_string('00000000111111110000111101010101') == 4
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read_binary_string(4) == '00000000111111110000111101010101'
    assert stream.tell() == 4
    stream.seek(0)
    with pytest.raises(ValueError):
        stream.write_binary_string('0000')


def test_align_to_2_byte():
    stream = Stream()
    stream.write(b'a')
    assert stream.align_to_2_byte_with_nulls() == 1
    assert stream.tell() == 2
    stream.seek(0)
    assert stream.read(2) == b'a\x00'


def test_align_to_4_byte():
    stream = Stream()
    stream.write(b'abc')
    assert stream.align_to_4_byte_with_nulls() == 1
    assert stream.tell() == 4
    stream.seek(0)
    assert stream.read(4) == b'abc\x00'


def test_get_value():
    stream = Stream(b'Hello World')
    assert stream.get_value() == b'Hello World'
