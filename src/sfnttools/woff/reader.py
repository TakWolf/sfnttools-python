from __future__ import annotations

from typing import Iterator

from sfnttools.configs import SfntConfigs
from sfnttools.payload import WoffPayload
from sfnttools.reader import SfntReader
from sfnttools.table import SfntTable
from sfnttools.tag import SfntVersion
from sfnttools.utils.stream import Stream
from sfnttools.woff.headers import WoffTableDirectoryEntry, WoffHeader
from sfnttools.xtf.headers import TableRecord, TableDirectory


class WoffReader(SfntReader):
    @staticmethod
    def create(stream: Stream, configs: SfntConfigs, verify_checksum: bool) -> WoffReader:
        stream.seek(0)
        header = WoffHeader.parse(stream)
        return WoffReader(stream, configs, header, verify_checksum)

    stream: Stream
    header: WoffHeader
    table_directory_entries_map: dict[str, WoffTableDirectoryEntry]

    def __init__(
            self,
            stream: Stream,
            configs: SfntConfigs,
            header: WoffHeader,
            verify_checksum: bool,
    ):
        super().__init__(configs, False, verify_checksum)
        self.stream = stream
        self.header = header
        self.table_directory_entries_map = {table_directory_entry.tag: table_directory_entry for table_directory_entry in header.table_directory_entries}

    def is_font_collection(self) -> bool:
        return False

    def get_sfnt_version(self) -> SfntVersion:
        return self.header.sfnt_version

    def get_table_tags(self) -> Iterator[str]:
        for table_directory_entry in self.header.table_directory_entries:
            yield table_directory_entry.tag

    def reconstruct_header_data(self) -> bytes:
        table_records = []
        offset = TableDirectory.calculate_bytes_size(self.header.num_tables)
        for table_directory_entry in sorted(self.header.table_directory_entries, key=lambda x: x.offset):
            table_records.append(TableRecord(
                table_directory_entry.tag,
                table_directory_entry.orig_checksum,
                offset,
                table_directory_entry.orig_length,
            ))
            offset += table_directory_entry.orig_length
            offset += 3 - (offset + 3) % 4
        table_records.sort(key=lambda x: x.tag)
        table_directory = TableDirectory.create(self.header.sfnt_version, table_records)

        stream = Stream()
        table_directory.dump(stream)
        return stream.get_value()

    def read_table_data_and_expected_checksum(self, tag: str) -> tuple[bytes, int | None]:
        table_directory_entry = self.table_directory_entries_map[tag]
        data = table_directory_entry.read_table_data(self.stream)
        expected_checksum = table_directory_entry.orig_checksum
        return data, expected_checksum

    def get_table_and_checksum_from_collection_cache(self, tag: str) -> tuple[SfntTable, int] | None:
        return None

    def set_table_and_checksum_to_collection_cache(self, tag: str, table: SfntTable, checksum: int):
        pass

    def read_woff_payload(self) -> WoffPayload | None:
        metadata = self.header.read_metadata(self.stream)
        private_data = self.header.read_private_data(self.stream)
        return WoffPayload(
            self.header.major_version,
            self.header.minor_version,
            metadata,
            private_data,
        )
