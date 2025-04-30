from enum import IntEnum
from io import BytesIO
from typing import Final

from sfnttools.error import SfntError
from sfnttools.table import SfntTableContainer, SfntTable
from sfnttools.utils.stream import Stream

_MAGIC_NUMBER = 0x5F0F3CF5

UNITS_PER_EM_MIN_VALUE: Final = 2 ** 4
UNITS_PER_EM_MAX_VALUE: Final = 2 ** 14


class FontDirectionHint(IntEnum):
    FULLY_MIXED = 0
    LEFT_TO_RIGHT = 1
    LEFT_TO_RIGHT_CONTAINS_NEUTRALS = 2
    RIGHT_TO_LEFT = -1
    RIGHT_TO_LEFT_CONTAINS_NEUTRALS = -2


class IndexToLocFormat(IntEnum):
    SHORT_OFFSETS = 0
    LONG_OFFSETS = 1


class GlyphDataFormat(IntEnum):
    CURRENT = 0


class HeadTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'HeadTable':
        stream = Stream(data)

        major_version = stream.read_uint16()
        minor_version = stream.read_uint16()
        font_revision = stream.read_fixed()
        checksum_adjustment = stream.read_uint32()
        magic_number = stream.read_uint32()
        if magic_number != _MAGIC_NUMBER:
            raise SfntError('bad magic number')
        flags = stream.read_uint16()
        units_per_em = stream.read_uint16()
        created_time = stream.read_long_datetime()
        modified_time = stream.read_long_datetime()
        x_min = stream.read_int16()
        y_min = stream.read_int16()
        x_max = stream.read_int16()
        y_max = stream.read_int16()
        mac_style = stream.read_uint16()
        lowest_rec_ppem = stream.read_uint16()
        font_direction_hint = FontDirectionHint(stream.read_int16())
        index_to_loc_format = IndexToLocFormat(stream.read_int16())
        glyph_data_format = GlyphDataFormat(stream.read_int16())

        return HeadTable(
            major_version,
            minor_version,
            font_revision,
            checksum_adjustment,
            flags,
            units_per_em,
            created_time,
            modified_time,
            x_min,
            y_min,
            x_max,
            y_max,
            mac_style,
            lowest_rec_ppem,
            font_direction_hint,
            index_to_loc_format,
            glyph_data_format,
        )

    major_version: int
    minor_version: int
    font_revision: float
    checksum_adjustment: int
    flags: int
    units_per_em: int
    created_time: int
    modified_time: int
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    mac_style: int
    lowest_rec_ppem: int
    font_direction_hint: FontDirectionHint
    index_to_loc_format: IndexToLocFormat
    glyph_data_format: GlyphDataFormat

    def __init__(
            self,
            major_version: int = 1,
            minor_version: int = 0,
            font_revision: float = 0,
            checksum_adjustment: int = 0,
            flags: int = 0,
            units_per_em: int = UNITS_PER_EM_MIN_VALUE,
            created_time: int = 0,
            modified_time: int = 0,
            x_min: int = 0,
            y_min: int = 0,
            x_max: int = 0,
            y_max: int = 0,
            mac_style: int = 0,
            lowest_rec_ppem: int = 0,
            font_direction_hint: FontDirectionHint = FontDirectionHint.LEFT_TO_RIGHT_CONTAINS_NEUTRALS,
            index_to_loc_format: IndexToLocFormat = IndexToLocFormat.SHORT_OFFSETS,
            glyph_data_format: GlyphDataFormat = GlyphDataFormat.CURRENT,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.font_revision = font_revision
        self.checksum_adjustment = checksum_adjustment
        self.flags = flags
        self.units_per_em = units_per_em
        self.created_time = created_time
        self.modified_time = modified_time
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.mac_style = mac_style
        self.lowest_rec_ppem = lowest_rec_ppem
        self.font_direction_hint = font_direction_hint
        self.index_to_loc_format = index_to_loc_format
        self.glyph_data_format = glyph_data_format

    def copy(self) -> 'HeadTable':
        return HeadTable(
            self.major_version,
            self.minor_version,
            self.font_revision,
            self.checksum_adjustment,
            self.flags,
            self.units_per_em,
            self.created_time,
            self.modified_time,
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
            self.mac_style,
            self.lowest_rec_ppem,
            self.font_direction_hint,
            self.index_to_loc_format,
            self.glyph_data_format,
        )

    def dump(self, container: SfntTableContainer) -> bytes:
        buffer = BytesIO()
        stream = Stream(buffer)

        stream.write_uint16(self.major_version)
        stream.write_uint16(self.minor_version)
        stream.write_fixed(self.font_revision)
        stream.write_uint32(self.checksum_adjustment)
        stream.write_uint32(_MAGIC_NUMBER)
        stream.write_uint16(self.flags)
        stream.write_uint16(self.units_per_em)
        stream.write_long_datetime(self.created_time)
        stream.write_long_datetime(self.modified_time)
        stream.write_int16(self.x_min)
        stream.write_int16(self.y_min)
        stream.write_int16(self.x_max)
        stream.write_int16(self.y_max)
        stream.write_uint16(self.mac_style)
        stream.write_uint16(self.lowest_rec_ppem)
        stream.write_int16(self.font_direction_hint)
        stream.write_int16(self.index_to_loc_format)
        stream.write_int16(self.glyph_data_format)

        return buffer.getvalue()
