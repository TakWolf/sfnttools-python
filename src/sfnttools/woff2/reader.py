from io import BytesIO
from typing import Iterator

from sfnttools.payload import TtcPayload, WoffPayload
from sfnttools.reader import SfntReader, SfntCollectionReader
from sfnttools.table import SfntTable
from sfnttools.tag import SfntVersion
from sfnttools.utils.stream import Stream
from sfnttools.woff2.headers import Woff2TableDirectoryEntry, Woff2CollectionFontEntry, Woff2Header
from sfnttools.xtf.headers import TableRecord, TableDirectory


class Woff2Reader(SfntReader):
    @staticmethod
    def create(stream: Stream, verify_checksum: bool) -> 'Woff2Reader':
        stream.seek(0)
        header = Woff2Header.parse(stream)
        font_entry = header.for_single_font_entry()
        uncompressed_stream = Stream(header.read_uncompressed_data(stream))
        return Woff2Reader(stream, uncompressed_stream, header, font_entry, None, False, verify_checksum)

    @staticmethod
    def create_by_ttc(stream: Stream, font_index: int) -> 'Woff2Reader':
        stream.seek(0)
        header = Woff2Header.parse(stream)
        font_entry = header.collection_header.font_entries[font_index]
        uncompressed_stream = Stream(header.read_uncompressed_data(stream))
        return Woff2Reader(stream, uncompressed_stream, header, font_entry, None, False, False)

    stream: Stream
    uncompressed_stream: Stream
    header: Woff2Header
    font_entry: Woff2CollectionFontEntry
    table_directory_entries_map: dict[str, Woff2TableDirectoryEntry]
    collection_tables_cache: dict[int, tuple[SfntTable, int]] | None

    def __init__(
            self,
            stream: Stream,
            uncompressed_stream: Stream,
            header: Woff2Header,
            font_entry: Woff2CollectionFontEntry,
            collection_tables_cache: dict[int, tuple[SfntTable, int]] | None,
            share_tables: bool,
            verify_checksum: bool,
    ):
        super().__init__(share_tables, verify_checksum)
        self.stream = stream
        self.uncompressed_stream = uncompressed_stream
        self.header = header
        self.font_entry = font_entry
        self.table_directory_entries_map = {table_directory_entry.tag: table_directory_entry for table_directory_entry in header.iter_table_directory_entries(font_entry)}
        self.collection_tables_cache = collection_tables_cache

    def is_font_collection(self) -> bool:
        return self.collection_tables_cache is not None

    def get_sfnt_version(self) -> SfntVersion:
        return self.font_entry.sfnt_version

    def get_table_tags(self) -> Iterator[str]:
        for table_directory_entry in self.header.iter_table_directory_entries(self.font_entry):
            yield table_directory_entry.tag

    def restore_header_data(self) -> bytes:
        table_records = []
        offset = TableDirectory.calculate_bytes_size(self.header.num_tables)
        for table_directory_entry in self.header.iter_table_directory_entries(self.font_entry):
            self.get_or_parse_table(table_directory_entry.tag)
            checksum = self.tables_cache[table_directory_entry.tag][1]
            table_records.append(TableRecord(
                table_directory_entry.tag,
                checksum,
                offset,
                table_directory_entry.orig_length,
            ))
            offset += table_directory_entry.orig_length
            offset += 3 - (offset + 3) % 4
        table_directory = TableDirectory.create(self.font_entry.sfnt_version, table_records)

        buffer = BytesIO()
        table_directory.dump(Stream(buffer))
        return buffer.getvalue()

    def read_table_data_and_expected_checksum(self, tag: str) -> tuple[bytes, int | None]:
        table_directory_entry = self.table_directory_entries_map[tag]
        data = table_directory_entry.read_table_data(self.uncompressed_stream)
        return data, None

    def get_table_and_checksum_from_collection_cache(self, tag: str) -> tuple[SfntTable, int] | None:
        if self.collection_tables_cache is not None:
            table_directory_entry = self.table_directory_entries_map[tag]
            return self.collection_tables_cache.get(table_directory_entry.offset, None)
        return None

    def set_table_and_checksum_to_collection_cache(self, tag: str, table: SfntTable, checksum: int):
        if self.collection_tables_cache is not None:
            table_directory_entry = self.table_directory_entries_map[tag]
            self.collection_tables_cache[table_directory_entry.offset] = table, checksum

    def read_woff_payload(self) -> WoffPayload | None:
        metadata = self.header.read_metadata(self.stream)
        private_data = self.header.read_private_data(self.stream)
        return WoffPayload(
            self.header.major_version,
            self.header.minor_version,
            metadata,
            private_data,
        )


class Woff2CollectionReader(SfntCollectionReader):
    @staticmethod
    def create(stream: Stream, share_tables: bool) -> 'Woff2CollectionReader':
        stream.seek(0)
        header = Woff2Header.parse(stream)
        uncompressed_stream = Stream(header.read_uncompressed_data(stream))
        return Woff2CollectionReader(stream, uncompressed_stream, header, share_tables)

    stream: Stream
    uncompressed_stream: Stream
    header: Woff2Header
    collection_tables_cache: dict[int, tuple[SfntTable, int]]
    share_tables: bool

    def __init__(
            self,
            stream: Stream,
            uncompressed_stream: Stream,
            header: Woff2Header,
            share_tables: bool,
    ):
        self.stream = stream
        self.uncompressed_stream = uncompressed_stream
        self.header = header
        self.collection_tables_cache = {}
        self.share_tables = share_tables

    def get_num_fonts(self) -> int:
        return self.header.collection_header.num_fonts

    def create_reader(self, font_index: int) -> SfntReader:
        font_entry = self.header.collection_header.font_entries[font_index]
        return Woff2Reader(
            self.stream,
            self.uncompressed_stream,
            self.header,
            font_entry,
            self.collection_tables_cache,
            self.share_tables,
            False,
        )

    def read_ttc_payload(self) -> TtcPayload:
        return TtcPayload()

    def read_woff_payload(self) -> WoffPayload | None:
        metadata = self.header.read_metadata(self.stream)
        private_data = self.header.read_private_data(self.stream)
        return WoffPayload(
            self.header.major_version,
            self.header.minor_version,
            metadata,
            private_data,
        )
