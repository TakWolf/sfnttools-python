import math

from sfnttools.error import SfntError
from sfnttools.tag import SfntVersion, SfntFileTag
from sfnttools.utils.stream import Stream


class TableRecord:
    @staticmethod
    def parse(stream: Stream) -> 'TableRecord':
        tag = stream.read_tag()
        checksum = stream.read_uint32()
        offset = stream.read_offset32()
        length = stream.read_uint32()
        return TableRecord(
            tag,
            checksum,
            offset,
            length,
        )

    tag: str
    checksum: int
    offset: int
    length: int

    def __init__(
            self,
            tag: str,
            checksum: int,
            offset: int,
            length: int,
    ):
        self.tag = tag
        self.checksum = checksum
        self.offset = offset
        self.length = length

    def read_table_data(self, stream: Stream) -> bytes:
        stream.seek(self.offset)
        data = stream.read(self.length)
        return data

    def dump(self, stream: Stream):
        stream.write_tag(self.tag)
        stream.write_uint32(self.checksum)
        stream.write_offset32(self.offset)
        stream.write_uint32(self.length)


class TableDirectory:
    @staticmethod
    def calculate_bytes_size(num_tables: int) -> int:
        return 4 + 2 + 2 + 2 + 2 + (4 + 4 + 4 + 4) * num_tables

    @staticmethod
    def create(sfnt_version: SfntVersion, table_records: list[TableRecord]) -> 'TableDirectory':
        num_tables = len(table_records)
        entry_selector = math.floor(math.log2(num_tables))
        search_range = 2 ** entry_selector * 16
        range_shift = num_tables * 16 - search_range
        return TableDirectory(sfnt_version, search_range, entry_selector, range_shift, table_records)

    @staticmethod
    def parse(stream: Stream) -> 'TableDirectory':
        sfnt_version = SfntVersion(stream.read_tag())
        num_tables = stream.read_uint16()
        search_range = stream.read_uint16()
        entry_selector = stream.read_uint16()
        range_shift = stream.read_uint16()
        table_records = [TableRecord.parse(stream) for _ in range(num_tables)]
        return TableDirectory(
            sfnt_version,
            search_range,
            entry_selector,
            range_shift,
            table_records,
        )

    sfnt_version: SfntVersion
    search_range: int
    entry_selector: int
    range_shift: int
    table_records: list[TableRecord]

    def __init__(
            self,
            sfnt_version: SfntVersion,
            search_range: int,
            entry_selector: int,
            range_shift: int,
            table_records: list[TableRecord],
    ):
        self.sfnt_version = sfnt_version
        self.search_range = search_range
        self.entry_selector = entry_selector
        self.range_shift = range_shift
        self.table_records = table_records

    @property
    def num_tables(self) -> int:
        return len(self.table_records)

    def dump(self, stream: Stream):
        stream.write_tag(self.sfnt_version)
        stream.write_uint16(self.num_tables)
        stream.write_uint16(self.search_range)
        stream.write_uint16(self.entry_selector)
        stream.write_uint16(self.range_shift)
        for table_record in self.table_records:
            table_record.dump(stream)


class TtcHeader:
    @staticmethod
    def parse(stream: Stream) -> 'TtcHeader':
        stream.read_tag()
        major_version = stream.read_uint16()
        minor_version = stream.read_uint16()
        num_fonts = stream.read_uint32()
        table_directory_offsets = [stream.read_offset32() for _ in range(num_fonts)]

        if (major_version, minor_version) == (1, 0):
            dsig_length = 0
            dsig_offset = 0
        elif (major_version, minor_version) == (2, 0):
            stream.read_tag()
            dsig_length = stream.read_uint32()
            dsig_offset = stream.read_uint32()
        else:
            raise SfntError(f'ttc header unsupported versions')

        return TtcHeader(
            major_version,
            minor_version,
            table_directory_offsets,
            dsig_length,
            dsig_offset,
        )

    major_version: int
    minor_version: int
    table_directory_offsets: list[int]
    dsig_length: int
    dsig_offset: int

    def __init__(
            self,
            major_version: int,
            minor_version: int,
            table_directory_offsets: list[int],
            dsig_length: int,
            dsig_offset: int,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.table_directory_offsets = table_directory_offsets
        self.dsig_length = dsig_length
        self.dsig_offset = dsig_offset

    @property
    def num_fonts(self) -> int:
        return len(self.table_directory_offsets)

    def read_table_directory(self, stream: Stream, font_index: int) -> tuple[TableDirectory, int]:
        table_directory_offset = self.table_directory_offsets[font_index]
        stream.seek(table_directory_offset)
        table_directory = TableDirectory.parse(stream)
        return table_directory, table_directory_offset

    def read_dsig_table_data(self, stream: Stream) -> bytes | None:
        if self.dsig_length == 0:
            return None

        stream.seek(self.dsig_offset)
        data = stream.read(self.dsig_length)
        return data

    def dump(self, stream: Stream):
        stream.write_tag(SfntFileTag.TTCF)
        stream.write_uint16(self.major_version)
        stream.write_uint16(self.minor_version)
        stream.write_uint32(self.num_fonts)
        for table_directory_offset in self.table_directory_offsets:
            stream.write_offset32(table_directory_offset)

        if (self.major_version, self.minor_version) == (1, 0):
            pass
        elif (self.major_version, self.minor_version) == (2, 0):
            stream.write_tag('DSIG' if self.dsig_length > 0 else '\x00\x00\x00\x00')
            stream.write_uint32(self.dsig_length)
            stream.write_uint32(self.dsig_offset)
        else:
            raise SfntError(f'ttc header unsupported versions')
