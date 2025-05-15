from typing import Iterator

from sfnttools.configs import SfntConfigs
from sfnttools.payload import TtcPayload, WoffPayload
from sfnttools.reader import SfntReader, SfntCollectionReader
from sfnttools.table import SfntTable
from sfnttools.tables.dsig.table import DsigTable
from sfnttools.tag import SfntVersion
from sfnttools.utils.stream import Stream
from sfnttools.xtf.headers import TableRecord, TableDirectory, TtcHeader


class XtfReader(SfntReader):
    @staticmethod
    def create(stream: Stream, configs: SfntConfigs, verify_checksum: bool) -> 'XtfReader':
        stream.seek(0)
        table_directory = TableDirectory.parse(stream)
        return XtfReader(stream, configs, table_directory, 0, None, False, verify_checksum)

    @staticmethod
    def create_by_ttc(stream: Stream, font_index: int, configs: SfntConfigs, verify_checksum: bool) -> 'XtfReader':
        stream.seek(0)
        header = TtcHeader.parse(stream)
        table_directory, table_directory_offset = header.read_table_directory(stream, font_index)
        return XtfReader(stream, configs, table_directory, table_directory_offset, None, False, verify_checksum)

    stream: Stream
    table_directory: TableDirectory
    table_directory_offset: int
    table_records_map: dict[str, TableRecord]
    collection_tables_cache: dict[tuple[str, int], tuple[SfntTable, int]] | None

    def __init__(
            self,
            stream: Stream,
            configs: SfntConfigs,
            table_directory: TableDirectory,
            table_directory_offset: int,
            collection_tables_cache: dict[tuple[str, int], tuple[SfntTable, int]] | None,
            share_tables: bool,
            verify_checksum: bool,
    ):
        super().__init__(configs, share_tables, verify_checksum)
        self.stream = stream
        self.table_directory = table_directory
        self.table_directory_offset = table_directory_offset
        self.table_records_map = {table_record.tag: table_record for table_record in table_directory.table_records}
        self.collection_tables_cache = collection_tables_cache

    def is_font_collection(self) -> bool:
        return self.collection_tables_cache is not None

    def get_sfnt_version(self) -> SfntVersion:
        return self.table_directory.sfnt_version

    def get_table_tags(self) -> Iterator[str]:
        for table_record in self.table_directory.table_records:
            yield table_record.tag

    def reconstruct_header_data(self) -> bytes:
        self.stream.seek(self.table_directory_offset)
        data = self.stream.read(TableDirectory.calculate_bytes_size(self.table_directory.num_tables))
        return data

    def read_table_data_and_expected_checksum(self, tag: str) -> tuple[bytes, int | None]:
        table_record = self.table_records_map[tag]
        data = table_record.read_table_data(self.stream)
        expected_checksum = table_record.checksum
        return data, expected_checksum

    def get_table_and_checksum_from_collection_cache(self, tag: str) -> tuple[SfntTable, int] | None:
        if self.collection_tables_cache is not None:
            table_record = self.table_records_map[tag]
            return self.collection_tables_cache.get((tag, table_record.offset), None)
        return None

    def set_table_and_checksum_to_collection_cache(self, tag: str, table: SfntTable, checksum: int):
        if self.collection_tables_cache is not None:
            table_record = self.table_records_map[tag]
            self.collection_tables_cache[(tag, table_record.offset)] = table, checksum

    def read_woff_payload(self) -> WoffPayload | None:
        return None


class XtfCollectionReader(SfntCollectionReader):
    @staticmethod
    def create(stream: Stream, configs: SfntConfigs, share_tables: bool, verify_checksum: bool) -> 'XtfCollectionReader':
        stream.seek(0)
        header = TtcHeader.parse(stream)
        return XtfCollectionReader(stream, configs, header, share_tables, verify_checksum)

    stream: Stream
    configs: SfntConfigs
    header: TtcHeader
    collection_tables_cache: dict[tuple[str, int], tuple[SfntTable, int]]
    share_tables: bool
    verify_checksum: bool

    def __init__(
            self,
            stream: Stream,
            configs: SfntConfigs,
            header: TtcHeader,
            share_tables: bool,
            verify_checksum: bool,
    ):
        self.stream = stream
        self.configs = configs
        self.header = header
        self.collection_tables_cache = {}
        self.share_tables = share_tables
        self.verify_checksum = verify_checksum

    @property
    def num_fonts(self) -> int:
        return self.header.num_fonts

    def create_reader(self, font_index: int) -> SfntReader:
        table_directory, table_directory_offset = self.header.read_table_directory(self.stream, font_index)
        return XtfReader(
            self.stream,
            self.configs,
            table_directory,
            table_directory_offset,
            self.collection_tables_cache,
            self.share_tables,
            self.verify_checksum,
        )

    def read_ttc_payload(self) -> TtcPayload:
        data = self.header.read_dsig_table_data(self.stream)
        dsig_table = None if data is None else DsigTable.parse(data, self.configs, {})
        return TtcPayload(
            self.header.major_version,
            self.header.minor_version,
            dsig_table,
        )

    def read_woff_payload(self) -> WoffPayload | None:
        return None
