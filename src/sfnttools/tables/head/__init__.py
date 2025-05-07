from datetime import datetime, timezone
from enum import IntEnum
from io import BytesIO
from typing import Final

from sfnttools.error import SfntError
from sfnttools.flags import SfntFlags
from sfnttools.table import SfntTableContainer, SfntTable
from sfnttools.utils.stream import Stream
from sfnttools.utils.time import seconds_since_1904_to_timestamp, timestamp_to_seconds_since_1904

_MAGIC_NUMBER = 0x5F0F3CF5

UNITS_PER_EM_MIN_VALUE: Final = 2 ** 4
UNITS_PER_EM_MAX_VALUE: Final = 2 ** 14

HEAD_TABLE_FLAGS_MASK_BASELINE_AT_Y0: Final = 0b_0000_0000_0000_0001
HEAD_TABLE_FLAGS_MASK_LEFT_SIDEBEARING_AT_X0: Final = 0b_0000_0000_0000_0010
HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_DEPEND_ON_POINT_SIZE: Final = 0b_0000_0000_0000_0100
HEAD_TABLE_FLAGS_MASK_FORCE_PPEM_TO_INTEGER: Final = 0b_0000_0000_0000_1000
HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_ALTER_ADVANCE_WIDTH: Final = 0b_0000_0000_0001_0000
HEAD_TABLE_FLAGS_MASK_FONT_DATA_IS_LOSSLESS_AFTER_OPTIMIZATION: Final = 0b_0000_1000_0000_0000
HEAD_TABLE_FLAGS_MASK_FONT_CONVERTED: Final = 0b_0001_0000_0000_0000
HEAD_TABLE_FLAGS_MASK_FONT_OPTIMIZED_FOR_CLEARTYPE: Final = 0b_0010_0000_0000_0000
HEAD_TABLE_FLAGS_MASK_LAST_RESORT_FONT: Final = 0b_0100_0000_0000_0000

MAC_STYLE_MASK_BOLD: Final = 0b_0000_0000_0000_0001
MAC_STYLE_MASK_ITALIC: Final = 0b_0000_0000_0000_0010
MAC_STYLE_MASK_UNDERLINE: Final = 0b_0000_0000_0000_0100
MAC_STYLE_MASK_OUTLINE: Final = 0b_0000_0000_0000_1000
MAC_STYLE_MASK_SHADOW: Final = 0b_0000_0000_0001_0000
MAC_STYLE_MASK_CONDENSED: Final = 0b_0000_0000_0010_0000
MAC_STYLE_MASK_EXTENDED: Final = 0b_0000_0000_0100_0000


class HeadTableFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'HeadTableFlags':
        baseline_at_y0 = value & HEAD_TABLE_FLAGS_MASK_BASELINE_AT_Y0 > 0
        left_sidebearing_at_x0 = value & HEAD_TABLE_FLAGS_MASK_LEFT_SIDEBEARING_AT_X0 > 0
        instructions_may_depend_on_point_size = value & HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_DEPEND_ON_POINT_SIZE > 0
        force_ppem_to_integer = value & HEAD_TABLE_FLAGS_MASK_FORCE_PPEM_TO_INTEGER > 0
        instructions_may_alter_advance_width = value & HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_ALTER_ADVANCE_WIDTH > 0
        font_data_is_lossless_after_optimization = value & HEAD_TABLE_FLAGS_MASK_FONT_DATA_IS_LOSSLESS_AFTER_OPTIMIZATION > 0
        font_converted = value & HEAD_TABLE_FLAGS_MASK_FONT_CONVERTED > 0
        font_optimized_for_cleartype = value & HEAD_TABLE_FLAGS_MASK_FONT_OPTIMIZED_FOR_CLEARTYPE > 0
        last_resort_font = value & HEAD_TABLE_FLAGS_MASK_LAST_RESORT_FONT > 0
        return HeadTableFlags(
            baseline_at_y0,
            left_sidebearing_at_x0,
            instructions_may_depend_on_point_size,
            force_ppem_to_integer,
            instructions_may_alter_advance_width,
            font_data_is_lossless_after_optimization,
            font_converted,
            font_optimized_for_cleartype,
            last_resort_font,
        )

    baseline_at_y0: bool
    left_sidebearing_at_x0: bool
    instructions_may_depend_on_point_size: bool
    force_ppem_to_integer: bool
    instructions_may_alter_advance_width: bool
    font_data_is_lossless_after_optimization: bool
    font_converted: bool
    font_optimized_for_cleartype: bool
    last_resort_font: bool

    def __init__(
            self,
            baseline_at_y0: bool = False,
            left_sidebearing_at_x0: bool = False,
            instructions_may_depend_on_point_size: bool = False,
            force_ppem_to_integer: bool = False,
            instructions_may_alter_advance_width: bool = False,
            font_data_is_lossless_after_optimization: bool = False,
            font_converted: bool = False,
            font_optimized_for_cleartype: bool = False,
            last_resort_font: bool = False,
    ):
        self.baseline_at_y0 = baseline_at_y0
        self.left_sidebearing_at_x0 = left_sidebearing_at_x0
        self.instructions_may_depend_on_point_size = instructions_may_depend_on_point_size
        self.force_ppem_to_integer = force_ppem_to_integer
        self.instructions_may_alter_advance_width = instructions_may_alter_advance_width
        self.font_data_is_lossless_after_optimization = font_data_is_lossless_after_optimization
        self.font_converted = font_converted
        self.font_optimized_for_cleartype = font_optimized_for_cleartype
        self.last_resort_font = last_resort_font

    @property
    def value(self) -> int:
        value = 0
        if self.baseline_at_y0:
            value |= HEAD_TABLE_FLAGS_MASK_BASELINE_AT_Y0
        if self.left_sidebearing_at_x0:
            value |= HEAD_TABLE_FLAGS_MASK_LEFT_SIDEBEARING_AT_X0
        if self.instructions_may_depend_on_point_size:
            value |= HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_DEPEND_ON_POINT_SIZE
        if self.force_ppem_to_integer:
            value |= HEAD_TABLE_FLAGS_MASK_FORCE_PPEM_TO_INTEGER
        if self.instructions_may_alter_advance_width:
            value |= HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_ALTER_ADVANCE_WIDTH
        if self.font_data_is_lossless_after_optimization:
            value |= HEAD_TABLE_FLAGS_MASK_FONT_DATA_IS_LOSSLESS_AFTER_OPTIMIZATION
        if self.font_converted:
            value |= HEAD_TABLE_FLAGS_MASK_FONT_CONVERTED
        if self.font_optimized_for_cleartype:
            value |= HEAD_TABLE_FLAGS_MASK_FONT_OPTIMIZED_FOR_CLEARTYPE
        if self.last_resort_font:
            value |= HEAD_TABLE_FLAGS_MASK_LAST_RESORT_FONT
        return value

    def copy(self) -> 'HeadTableFlags':
        return HeadTableFlags(
            self.baseline_at_y0,
            self.left_sidebearing_at_x0,
            self.instructions_may_depend_on_point_size,
            self.force_ppem_to_integer,
            self.instructions_may_alter_advance_width,
            self.font_data_is_lossless_after_optimization,
            self.font_converted,
            self.font_optimized_for_cleartype,
            self.last_resort_font,
        )


class MacStyle(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'MacStyle':
        bold = value & MAC_STYLE_MASK_BOLD > 0
        italic = value & MAC_STYLE_MASK_ITALIC > 0
        underline = value & MAC_STYLE_MASK_UNDERLINE > 0
        outline = value & MAC_STYLE_MASK_OUTLINE > 0
        shadow = value & MAC_STYLE_MASK_SHADOW > 0
        condensed = value & MAC_STYLE_MASK_CONDENSED > 0
        extended = value & MAC_STYLE_MASK_EXTENDED > 0
        return MacStyle(
            bold,
            italic,
            underline,
            outline,
            shadow,
            condensed,
            extended,
        )

    bold: bool
    italic: bool
    underline: bool
    outline: bool
    shadow: bool
    condensed: bool
    extended: bool

    def __init__(
            self,
            bold: bool = False,
            italic: bool = False,
            underline: bool = False,
            outline: bool = False,
            shadow: bool = False,
            condensed: bool = False,
            extended: bool = False,
    ):
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.outline = outline
        self.shadow = shadow
        self.condensed = condensed
        self.extended = extended

    @property
    def value(self) -> int:
        value = 0
        if self.bold:
            value |= MAC_STYLE_MASK_BOLD
        if self.italic:
            value |= MAC_STYLE_MASK_ITALIC
        if self.underline:
            value |= MAC_STYLE_MASK_UNDERLINE
        if self.outline:
            value |= MAC_STYLE_MASK_OUTLINE
        if self.shadow:
            value |= MAC_STYLE_MASK_SHADOW
        if self.condensed:
            value |= MAC_STYLE_MASK_CONDENSED
        if self.extended:
            value |= MAC_STYLE_MASK_EXTENDED
        return value

    def copy(self) -> 'MacStyle':
        return MacStyle(
            self.bold,
            self.italic,
            self.underline,
            self.outline,
            self.shadow,
            self.condensed,
            self.extended,
        )


class FontDirectionHint(IntEnum):
    FULLY_MIXED = 0
    LEFT_TO_RIGHT = 1
    LEFT_TO_RIGHT_CONTAINS_NEUTRALS = 2
    RIGHT_TO_LEFT = -1
    RIGHT_TO_LEFT_CONTAINS_NEUTRALS = -2


class IndexToLocFormat(IntEnum):
    SHORT = 0
    LONG = 1


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
        flags = HeadTableFlags.parse(stream.read_uint16())
        units_per_em = stream.read_uint16()
        created_seconds_since_1904 = stream.read_long_datetime()
        modified_seconds_since_1904 = stream.read_long_datetime()
        x_min = stream.read_int16()
        y_min = stream.read_int16()
        x_max = stream.read_int16()
        y_max = stream.read_int16()
        mac_style = MacStyle.parse(stream.read_uint16())
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
            created_seconds_since_1904,
            modified_seconds_since_1904,
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
    flags: HeadTableFlags
    units_per_em: int
    created_seconds_since_1904: int
    modified_seconds_since_1904: int
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    mac_style: MacStyle
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
            flags: HeadTableFlags | None = None,
            units_per_em: int = UNITS_PER_EM_MIN_VALUE,
            created_seconds_since_1904: int = 0,
            modified_seconds_since_1904: int = 0,
            x_min: int = 0,
            y_min: int = 0,
            x_max: int = 0,
            y_max: int = 0,
            mac_style: MacStyle | None = None,
            lowest_rec_ppem: int = 0,
            font_direction_hint: FontDirectionHint = FontDirectionHint.LEFT_TO_RIGHT_CONTAINS_NEUTRALS,
            index_to_loc_format: IndexToLocFormat = IndexToLocFormat.SHORT,
            glyph_data_format: GlyphDataFormat = GlyphDataFormat.CURRENT,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.font_revision = font_revision
        self.checksum_adjustment = checksum_adjustment
        self.flags = HeadTableFlags() if flags is None else flags
        self.units_per_em = units_per_em
        self.created_seconds_since_1904 = created_seconds_since_1904
        self.modified_seconds_since_1904 = modified_seconds_since_1904
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.mac_style = MacStyle() if mac_style is None else mac_style
        self.lowest_rec_ppem = lowest_rec_ppem
        self.font_direction_hint = font_direction_hint
        self.index_to_loc_format = index_to_loc_format
        self.glyph_data_format = glyph_data_format

    @property
    def created_timestamp(self) -> int:
        return seconds_since_1904_to_timestamp(self.created_seconds_since_1904)

    @created_timestamp.setter
    def created_timestamp(self, value: int):
        self.created_seconds_since_1904 = timestamp_to_seconds_since_1904(value)

    @property
    def created_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.created_timestamp, timezone.utc)

    @created_datetime.setter
    def created_datetime(self, value: datetime):
        self.created_timestamp = int(value.timestamp())

    @property
    def modified_timestamp(self) -> int:
        return seconds_since_1904_to_timestamp(self.modified_seconds_since_1904)

    @modified_timestamp.setter
    def modified_timestamp(self, value: int):
        self.modified_seconds_since_1904 = timestamp_to_seconds_since_1904(value)

    @property
    def modified_datetime(self) -> datetime:
        return datetime.fromtimestamp(self.modified_timestamp, timezone.utc)

    @modified_datetime.setter
    def modified_datetime(self, value: datetime):
        self.modified_timestamp = int(value.timestamp())

    def copy(self) -> 'HeadTable':
        return HeadTable(
            self.major_version,
            self.minor_version,
            self.font_revision,
            self.checksum_adjustment,
            self.flags.copy(),
            self.units_per_em,
            self.created_seconds_since_1904,
            self.modified_seconds_since_1904,
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
            self.mac_style.copy(),
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
        stream.write_uint16(self.flags.value)
        stream.write_uint16(self.units_per_em)
        stream.write_long_datetime(self.created_seconds_since_1904)
        stream.write_long_datetime(self.modified_seconds_since_1904)
        stream.write_int16(self.x_min)
        stream.write_int16(self.y_min)
        stream.write_int16(self.x_max)
        stream.write_int16(self.y_max)
        stream.write_uint16(self.mac_style.value)
        stream.write_uint16(self.lowest_rec_ppem)
        stream.write_int16(self.font_direction_hint)
        stream.write_int16(self.index_to_loc_format)
        stream.write_int16(self.glyph_data_format)

        return buffer.getvalue()
