from __future__ import annotations

import zlib

from sfnttools.error import SfntError
from sfnttools.tag import SfntVersion, SfntFileTag
from sfnttools.utils.stream import Stream


class WoffTableDirectoryEntry:
    @staticmethod
    def parse(stream: Stream) -> WoffTableDirectoryEntry:
        tag = stream.read_tag()
        offset = stream.read_uint32()
        comp_length = stream.read_uint32()
        orig_length = stream.read_uint32()
        orig_checksum = stream.read_uint32()
        return WoffTableDirectoryEntry(
            tag,
            offset,
            comp_length,
            orig_length,
            orig_checksum,
        )

    tag: str
    offset: int
    comp_length: int
    orig_length: int
    orig_checksum: int

    def __init__(
            self,
            tag: str,
            offset: int,
            comp_length: int,
            orig_length: int,
            orig_checksum: int,
    ):
        self.tag = tag
        self.offset = offset
        self.comp_length = comp_length
        self.orig_length = orig_length
        self.orig_checksum = orig_checksum

    def read_table_data(self, stream: Stream) -> bytes:
        stream.seek(self.offset)
        data = stream.read(self.comp_length)
        if self.orig_length > self.comp_length:
            data = zlib.decompress(data)
            if len(data) != self.orig_length:
                raise SfntError(f'woff table {repr(self.tag)} bad data length')
        return data

    def dump(self, stream: Stream):
        stream.write_tag(self.tag)
        stream.write_uint32(self.offset)
        stream.write_uint32(self.comp_length)
        stream.write_uint32(self.orig_length)
        stream.write_uint32(self.orig_checksum)


class WoffHeader:
    @staticmethod
    def parse(stream: Stream) -> WoffHeader:
        stream.read_tag()
        sfnt_version = SfntVersion(stream.read_tag())
        length = stream.read_uint32()
        num_tables = stream.read_uint16()
        stream.read_uint16()
        total_sfnt_size = stream.read_uint32()
        major_version = stream.read_uint16()
        minor_version = stream.read_uint16()
        meta_offset = stream.read_uint32()
        meta_length = stream.read_uint32()
        meta_orig_length = stream.read_uint32()
        priv_offset = stream.read_uint32()
        priv_length = stream.read_uint32()
        table_directory_entries = [WoffTableDirectoryEntry.parse(stream) for _ in range(num_tables)]
        return WoffHeader(
            sfnt_version,
            length,
            total_sfnt_size,
            major_version,
            minor_version,
            meta_offset,
            meta_length,
            meta_orig_length,
            priv_offset,
            priv_length,
            table_directory_entries,
        )

    sfnt_version: SfntVersion
    length: int
    total_sfnt_size: int
    major_version: int
    minor_version: int
    meta_offset: int
    meta_length: int
    meta_orig_length: int
    priv_offset: int
    priv_length: int
    table_directory_entries: list[WoffTableDirectoryEntry]

    def __init__(
            self,
            sfnt_version: SfntVersion,
            length: int,
            total_sfnt_size: int,
            major_version: int,
            minor_version: int,
            meta_offset: int,
            meta_length: int,
            meta_orig_length: int,
            priv_offset: int,
            priv_length: int,
            table_directory_entries: list[WoffTableDirectoryEntry],
    ):
        self.sfnt_version = sfnt_version
        self.length = length
        self.total_sfnt_size = total_sfnt_size
        self.major_version = major_version
        self.minor_version = minor_version
        self.meta_offset = meta_offset
        self.meta_length = meta_length
        self.meta_orig_length = meta_orig_length
        self.priv_offset = priv_offset
        self.priv_length = priv_length
        self.table_directory_entries = table_directory_entries

    @property
    def num_tables(self) -> int:
        return len(self.table_directory_entries)

    def read_metadata(self, stream: Stream) -> bytes | None:
        if self.meta_length == 0:
            return None

        stream.seek(self.meta_offset)
        data = stream.read(self.meta_length)
        data = zlib.decompress(data)
        if len(data) != self.meta_orig_length:
            raise SfntError(f'woff bad metadata length')
        return data

    def read_private_data(self, stream: Stream) -> bytes | None:
        if self.priv_length == 0:
            return None

        stream.seek(self.priv_offset)
        data = stream.read(self.priv_length)
        return data

    def dump(self, stream: Stream):
        stream.write_tag(SfntFileTag.WOFF)
        stream.write_tag(self.sfnt_version)
        stream.write_uint32(self.length)
        stream.write_uint16(self.num_tables)
        stream.write_uint16(0)
        stream.write_uint32(self.total_sfnt_size)
        stream.write_uint16(self.major_version)
        stream.write_uint16(self.minor_version)
        stream.write_uint32(self.meta_offset)
        stream.write_uint32(self.meta_length)
        stream.write_uint32(self.meta_orig_length)
        stream.write_uint32(self.priv_offset)
        stream.write_uint32(self.priv_length)
        for table_directory_entry in self.table_directory_entries:
            table_directory_entry.dump(stream)
