from __future__ import annotations

from datetime import datetime, timezone
from typing import Final, Any

from sfnttools.configs import SfntConfigs
from sfnttools.error import SfntError
from sfnttools.table import SfntTable
from sfnttools.tables.head.enum import FontDirectionHint, IndexToLocFormat, GlyphDataFormat
from sfnttools.tables.head.flags import HeadTableFlags, MacStyle
from sfnttools.utils.stream import Stream
from sfnttools.utils.time import seconds_since_1904_to_timestamp, timestamp_to_seconds_since_1904

_MAGIC_NUMBER = 0x5F0F3CF5

UNITS_PER_EM_MIN_VALUE: Final = 2 ** 4
UNITS_PER_EM_MAX_VALUE: Final = 2 ** 14


class HeadTable(SfntTable):
    update_dependencies = ['CFF ', 'CFF2', 'glyf', 'loca']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> HeadTable:
        stream = Stream(data)

        major_version = stream.read_uint16()
        minor_version = stream.read_uint16()
        font_revision = stream.read_fixed()
        checksum_adjustment = stream.read_uint32()
        magic_number = stream.read_uint32()
        if magic_number != _MAGIC_NUMBER:
            raise SfntError('[head] bad magic number')
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
            units_per_em: int = 1024,
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

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HeadTable):
            return False
        return (self.major_version == other.major_version and
                self.minor_version == other.minor_version and
                self.font_revision == other.font_revision and
                self.checksum_adjustment == other.checksum_adjustment and
                self.flags == other.flags and
                self.units_per_em == other.units_per_em and
                self.created_seconds_since_1904 == other.created_seconds_since_1904 and
                self.modified_seconds_since_1904 == other.modified_seconds_since_1904 and
                self.x_min == other.x_min and
                self.y_min == other.y_min and
                self.x_max == other.x_max and
                self.y_max == other.y_max and
                self.mac_style == other.mac_style and
                self.lowest_rec_ppem == other.lowest_rec_ppem and
                self.font_direction_hint == other.font_direction_hint and
                self.index_to_loc_format == other.index_to_loc_format and
                self.glyph_data_format == other.glyph_data_format)

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

    def copy(self) -> HeadTable:
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

    def update(self, configs: SfntConfigs, tables: dict[str, SfntTable]):
        from sfnttools.tables.cff_.table import CffTable
        cff_table: CffTable | None = dependencies.get('CFF ', None)
        from sfnttools.tables.cff2.table import Cff2Table
        cff2_table: Cff2Table | None = dependencies.get('CFF2', None)
        from sfnttools.tables.glyf.table import GlyfTable
        glyf_table: GlyfTable | None = dependencies.get('glyf', None)

        if cff_table is not None:
            self.x_min, self.y_min, self.x_max, self.y_max = cff_table.calculate_bounds_box()
        elif cff2_table is not None:
            self.x_min, self.y_min, self.x_max, self.y_max = cff2_table.calculate_bounds_box()
        elif glyf_table is not None:
            self.x_min, self.y_min, self.x_max, self.y_max = glyf_table.calculate_bounds_box()

            from sfnttools.tables.loca.table import LocaTable
            loca_table: LocaTable = dependencies['loca']

            self.index_to_loc_format = loca_table.calculate_index_to_loc_format()

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        stream = Stream()

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

        return stream.get_value(), {}
