from __future__ import annotations

from collections.abc import Iterator

import brotli

from sfnttools.error import SfntError
from sfnttools.tag import SfntVersion, SfntFileTag
from sfnttools.utils.stream import Stream

_KNOWN_TABLE_TAGS = [
    'cmap',
    'head',
    'hhea',
    'hmtx',
    'maxp',
    'name',
    'OS/2',
    'post',
    'cvt ',
    'fpgm',
    'glyf',
    'loca',
    'prep',
    'CFF ',
    'VORG',
    'EBDT',
    'EBLC',
    'gasp',
    'hdmx',
    'kern',
    'LTSH',
    'PCLT',
    'VDMX',
    'vhea',
    'vmtx',
    'BASE',
    'GDEF',
    'GPOS',
    'GSUB',
    'EBSC',
    'JSTF',
    'MATH',
    'CBDT',
    'CBLC',
    'COLR',
    'CPAL',
    'SVG ',
    'sbix',
    'acnt',
    'avar',
    'bdat',
    'bloc',
    'bsln',
    'cvar',
    'fdsc',
    'feat',
    'fmtx',
    'fvar',
    'gvar',
    'hsty',
    'just',
    'lcar',
    'mort',
    'morx',
    'opbd',
    'prop',
    'trak',
    'Zapf',
    'Silf',
    'Glat',
    'Gloc',
    'Feat',
    'Sill',
]


class Woff2TableDirectoryEntryFlags:
    @staticmethod
    def parse(stream: Stream) -> Woff2TableDirectoryEntryFlags:
        value = stream.read_uint8()

        tag_index = value & 0b_0011_1111
        if tag_index < len(_KNOWN_TABLE_TAGS):
            tag = _KNOWN_TABLE_TAGS[tag_index]
        else:
            tag = stream.read_tag()

        transform_version = value >> 6
        if tag in ('glyf', 'loca'):
            transformed = transform_version != 3
        else:
            transformed = transform_version != 0

        return Woff2TableDirectoryEntryFlags(tag, transformed)

    tag: str
    transformed: bool

    def __init__(
            self,
            tag: str,
            transformed: bool,
    ):
        self.tag = tag
        self.transformed = transformed

    def dump(self, stream: Stream):
        try:
            tag_index = _KNOWN_TABLE_TAGS.index(self.tag)
        except ValueError:
            tag_index = len(_KNOWN_TABLE_TAGS)

        if self.tag in ('glyf', 'loca'):
            transform_version = 0 if self.transformed else 3
        else:
            transform_version = 1 if self.transformed else 0

        value = transform_version << 6 | tag_index
        stream.write_uint8(value)
        if tag_index == len(_KNOWN_TABLE_TAGS):
            stream.write_tag(self.tag)


class Woff2TableDirectoryEntry:
    @staticmethod
    def parse(stream: Stream, offset: int) -> Woff2TableDirectoryEntry:
        flags = Woff2TableDirectoryEntryFlags.parse(stream)
        orig_length = stream.read_uint_base128()
        if flags.transformed:
            transform_length = stream.read_uint_base128()
            if flags.tag == 'loca' and transform_length != 0:
                raise SfntError("woff2 transformed table 'loca' length must be 0")
        else:
            transform_length = None
        return Woff2TableDirectoryEntry(
            flags.tag,
            offset,
            orig_length,
            transform_length,
        )

    tag: str
    offset: int
    orig_length: int
    transform_length: int | None

    def __init__(
            self,
            tag: str,
            offset: int,
            orig_length: int,
            transform_length: int | None,
    ):
        self.tag = tag
        self.offset = offset
        self.orig_length = orig_length
        self.transform_length = transform_length

    @property
    def transformed(self) -> bool:
        return self.transform_length is not None

    @property
    def length(self) -> int:
        return self.orig_length if self.transform_length is None else self.transform_length

    def read_table_data(self, uncompressed_stream: Stream) -> bytes:
        uncompressed_stream.seek(self.offset)
        data = uncompressed_stream.read(self.length)
        return data

    def dump(self, stream: Stream):
        Woff2TableDirectoryEntryFlags(self.tag, self.transformed).dump(stream)
        stream.write_uint_base128(self.orig_length)
        if self.transform_length is not None:
            if self.tag == 'loca' and self.transform_length != 0:
                raise SfntError("woff2 transformed table 'loca' length must be 0")
            stream.write_uint_base128(self.transform_length)


class Woff2CollectionFontEntry:
    @staticmethod
    def parse(stream: Stream) -> Woff2CollectionFontEntry:
        num_tables = stream.read_255uint16()
        sfnt_version = SfntVersion(stream.read_tag())
        indices = [stream.read_255uint16() for _ in range(num_tables)]
        return Woff2CollectionFontEntry(
            sfnt_version,
            indices,
        )

    sfnt_version: SfntVersion
    indices: list[int]

    def __init__(
            self,
            sfnt_version: SfntVersion,
            indices: list[int],
    ):
        self.sfnt_version = sfnt_version
        self.indices = indices

    @property
    def num_tables(self) -> int:
        return len(self.indices)

    def dump(self, stream: Stream):
        stream.write_255uint16(self.num_tables)
        stream.write_tag(self.sfnt_version)
        for index in self.indices:
            stream.write_255uint16(index)


class Woff2CollectionHeader:
    @staticmethod
    def parse(stream: Stream) -> Woff2CollectionHeader:
        major_version = stream.read_uint16()
        minor_version = stream.read_uint16()
        num_fonts = stream.read_255uint16()
        font_entries = [Woff2CollectionFontEntry.parse(stream) for _ in range(num_fonts)]
        return Woff2CollectionHeader(
            major_version,
            minor_version,
            font_entries,
        )

    major_version: int
    minor_version: int
    font_entries: list[Woff2CollectionFontEntry]

    def __init__(
            self,
            major_version: int,
            minor_version: int,
            font_entries: list[Woff2CollectionFontEntry],
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.font_entries = font_entries

    @property
    def num_fonts(self) -> int:
        return len(self.font_entries)

    def dump(self, stream: Stream):
        stream.write_uint16(self.major_version)
        stream.write_uint16(self.minor_version)
        stream.write_255uint16(self.num_fonts)
        for font_entry in self.font_entries:
            font_entry.dump(stream)


class Woff2Header:
    @staticmethod
    def parse(stream: Stream) -> Woff2Header:
        stream.read_tag()
        flavor = stream.read_tag()
        length = stream.read_uint32()
        num_tables = stream.read_uint16()
        stream.read_uint16()
        total_sfnt_size = stream.read_uint32()
        total_compressed_size = stream.read_uint32()
        major_version = stream.read_uint16()
        minor_version = stream.read_uint16()
        meta_offset = stream.read_uint32()
        meta_length = stream.read_uint32()
        meta_orig_length = stream.read_uint32()
        priv_offset = stream.read_uint32()
        priv_length = stream.read_uint32()
        table_directory_entries = []
        total_uncompressed_size = 0
        for _ in range(num_tables):
            table_directory_entry = Woff2TableDirectoryEntry.parse(stream, total_uncompressed_size)
            table_directory_entries.append(table_directory_entry)
            total_uncompressed_size += table_directory_entry.length
        collection_header = Woff2CollectionHeader.parse(stream) if flavor == SfntFileTag.TTCF else None
        compressed_data_offset = stream.tell()
        return Woff2Header(
            flavor,
            length,
            total_sfnt_size,
            compressed_data_offset,
            total_compressed_size,
            total_uncompressed_size,
            major_version,
            minor_version,
            meta_offset,
            meta_length,
            meta_orig_length,
            priv_offset,
            priv_length,
            table_directory_entries,
            collection_header,
        )

    flavor: str
    length: int
    total_sfnt_size: int
    compressed_data_offset: int
    total_compressed_size: int
    total_uncompressed_size: int
    major_version: int
    minor_version: int
    meta_offset: int
    meta_length: int
    meta_orig_length: int
    priv_offset: int
    priv_length: int
    table_directory_entries: list[Woff2TableDirectoryEntry]
    collection_header: Woff2CollectionHeader | None

    def __init__(
            self,
            flavor: str,
            length: int,
            total_sfnt_size: int,
            compressed_data_offset: int,
            total_compressed_size: int,
            total_uncompressed_size: int,
            major_version: int,
            minor_version: int,
            meta_offset: int,
            meta_length: int,
            meta_orig_length: int,
            priv_offset: int,
            priv_length: int,
            table_directory_entries: list[Woff2TableDirectoryEntry],
            collection_header: Woff2CollectionHeader | None,
    ):
        self.flavor = flavor
        self.length = length
        self.total_sfnt_size = total_sfnt_size
        self.compressed_data_offset = compressed_data_offset
        self.total_compressed_size = total_compressed_size
        self.total_uncompressed_size = total_uncompressed_size
        self.major_version = major_version
        self.minor_version = minor_version
        self.meta_offset = meta_offset
        self.meta_length = meta_length
        self.meta_orig_length = meta_orig_length
        self.priv_offset = priv_offset
        self.priv_length = priv_length
        self.table_directory_entries = table_directory_entries
        self.collection_header = collection_header

    @property
    def num_tables(self) -> int:
        return len(self.table_directory_entries)

    def read_uncompressed_data(self, stream: Stream) -> bytes:
        stream.seek(self.compressed_data_offset)
        data = stream.read(self.total_compressed_size)
        data = brotli.decompress(data)
        if len(data) != self.total_uncompressed_size:
            raise SfntError(f'woff2 bad uncompressed data size')
        return data

    def for_single_font_entry(self) -> Woff2CollectionFontEntry:
        sfnt_version = SfntVersion(self.flavor)
        indices = [i for i in range(self.num_tables)]
        return Woff2CollectionFontEntry(sfnt_version, indices)

    def iter_table_directory_entries(self, font_entry: Woff2CollectionFontEntry) -> Iterator[Woff2TableDirectoryEntry]:
        for index in font_entry.indices:
            table_directory_entry = self.table_directory_entries[index]
            yield table_directory_entry

    def read_metadata(self, stream: Stream) -> bytes | None:
        if self.meta_length == 0:
            return None

        stream.seek(self.meta_offset)
        data = stream.read(self.meta_length)
        data = brotli.decompress(data)
        if len(data) != self.meta_orig_length:
            raise SfntError(f'woff2 bad metadata length')
        return data

    def read_private_data(self, stream: Stream) -> bytes | None:
        if self.priv_length == 0:
            return None

        stream.seek(self.priv_offset)
        data = stream.read(self.priv_length)
        return data

    def dump(self, stream: Stream):
        stream.write_tag(SfntFileTag.WOFF2)
        stream.write_tag(self.flavor)
        stream.write_uint32(self.length)
        stream.write_uint16(self.num_tables)
        stream.write_uint16(0)
        stream.write_uint32(self.total_sfnt_size)
        stream.write_uint32(self.total_compressed_size)
        stream.write_uint16(self.major_version)
        stream.write_uint16(self.minor_version)
        stream.write_uint32(self.meta_offset)
        stream.write_uint32(self.meta_length)
        stream.write_uint32(self.meta_orig_length)
        stream.write_uint32(self.priv_offset)
        stream.write_uint32(self.priv_length)
        for table_directory_entry in self.table_directory_entries:
            table_directory_entry.dump(stream)
        if self.collection_header is not None:
            self.collection_header.dump(stream)
