from collections import UserDict, UserList
from io import BytesIO
from os import PathLike
from typing import Any, BinaryIO

from sfnttools.configs import SfntConfigs
from sfnttools.error import SfntError
from sfnttools.payload import TtcPayload, WoffPayload
from sfnttools.table import SfntTable
from sfnttools.tables.factory import TABLE_TYPE_REGISTRY
from sfnttools.tag import SfntVersion, SfntFileTag
from sfnttools.utils.stream import Stream
from sfnttools.woff.reader import WoffReader
from sfnttools.woff2.reader import Woff2Reader, Woff2CollectionReader
from sfnttools.xtf.reader import XtfReader, XtfCollectionReader


class SfntFont(UserDict[str, SfntTable]):
    @staticmethod
    def parse(
            stream: bytes | bytearray | BinaryIO,
            configs: SfntConfigs | None = None,
            font_index: int | None = None,
            verify_checksum: bool = False,
    ) -> 'SfntFont':
        if isinstance(stream, (bytes, bytearray)):
            stream = BytesIO(stream)
        stream = Stream(stream)

        if configs is None:
            configs = SfntConfigs()

        stream.seek(0)
        tag = stream.read_tag()
        if tag == SfntFileTag.TTCF:
            if font_index is None:
                raise SfntError(f'must specify a font index in font collection')
            reader = XtfReader.create_by_ttc(stream, configs, font_index, verify_checksum)
        elif tag == SfntFileTag.WOFF:
            reader = WoffReader.create(stream, configs, verify_checksum)
        elif tag == SfntFileTag.WOFF2:
            stream.seek(4)
            flavor = stream.read_tag()
            if flavor == SfntFileTag.TTCF:
                if font_index is None:
                    raise SfntError(f'must specify a font index in font collection')
                reader = Woff2Reader.create_by_ttc(stream, configs, font_index)
            elif flavor in [*SfntVersion]:
                reader = Woff2Reader.create(stream, configs)
            else:
                raise SfntError('unsupported font')
        elif tag in [*SfntVersion]:
            reader = XtfReader.create(stream, configs, verify_checksum)
        else:
            raise SfntError('unsupported font')

        sfnt_version, tables = reader.parse_font()
        woff_payload = reader.read_woff_payload()
        return SfntFont(sfnt_version, tables, woff_payload)

    @staticmethod
    def load(
            file_path: str | PathLike[str],
            configs: SfntConfigs | None = None,
            font_index: int | None = None,
            verify_checksum: bool = False,
    ) -> 'SfntFont':
        with open(file_path, 'rb') as file:
            return SfntFont.parse(file, configs, font_index, verify_checksum)

    sfnt_version: SfntVersion
    woff_payload: WoffPayload | None

    def __init__(
            self,
            sfnt_version: SfntVersion,
            tables: dict[str, SfntTable] | None = None,
            woff_payload: WoffPayload | None = None,
    ):
        super().__init__(tables)
        self.sfnt_version = sfnt_version
        self.woff_payload = woff_payload

    def __setitem__(self, tag: Any, table: Any):
        if not isinstance(tag, str):
            raise KeyError("tag must be a 'str'")

        if len(tag) != 4:
            raise KeyError('tag length must be 4')

        if any(not 0x20 <= ord(c) <= 0x7E for c in tag):
            raise KeyError('tag contains illegal characters')

        if tag.startswith(' '):
            raise KeyError('tag cannot start with a space')

        if ' ' in tag.strip():
            raise KeyError('tag cannot contain spaces in between')

        table_type = TABLE_TYPE_REGISTRY.get(tag, SfntTable)
        if not isinstance(table, table_type):
            raise ValueError(f'bad table type for tag {repr(tag)}')

        super().__setitem__(tag, table)

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SfntFont):
            return False
        return (self.sfnt_version == other.sfnt_version and
                self.woff_payload == other.woff_payload and
                super().__eq__(other))

    def copy(self) -> 'SfntFont':
        tables = {tag: table.copy() for tag, table in self.items()}
        return SfntFont(
            self.sfnt_version,
            tables,
            self.woff_payload.copy(),
        )


class SfntFontCollection(UserList[SfntFont]):
    @staticmethod
    def parse(
            stream: bytes | bytearray | BinaryIO,
            configs: SfntConfigs | None = None,
            share_tables: bool = True,
            verify_checksum: bool = False,
    ) -> 'SfntFontCollection':
        if isinstance(stream, (bytes, bytearray)):
            stream = BytesIO(stream)
        stream = Stream(stream)

        if configs is None:
            configs = SfntConfigs()

        stream.seek(0)
        tag = stream.read_tag()
        if tag == SfntFileTag.TTCF:
            collection_reader = XtfCollectionReader.create(stream, configs, share_tables, verify_checksum)
        elif tag == SfntFileTag.WOFF2:
            stream.seek(4)
            flavor = stream.read_tag()
            if flavor != SfntFileTag.TTCF:
                raise SfntError('not a woff2 collection font')
            collection_reader = Woff2CollectionReader.create(stream, configs, share_tables)
        else:
            raise SfntError('unsupported collection font')

        fonts = []
        for font_index in range(collection_reader.num_fonts):
            reader = collection_reader.create_reader(font_index)
            sfnt_version, tables = reader.parse_font()
            fonts.append(SfntFont(sfnt_version, tables))
        woff_payload = collection_reader.read_woff_payload()
        return SfntFontCollection(fonts, woff_payload)

    @staticmethod
    def load(
            file_path: str | PathLike[str],
            configs: SfntConfigs | None = None,
            share_tables: bool = True,
            verify_checksum: bool = False,
    ) -> 'SfntFontCollection':
        with open(file_path, 'rb') as file:
            return SfntFontCollection.parse(file, configs, share_tables, verify_checksum)

    ttc_payload: TtcPayload
    woff_payload: WoffPayload | None

    def __init__(
            self,
            fonts: list[SfntFont] | None = None,
            ttc_payload: TtcPayload | None = None,
            woff_payload: WoffPayload | None = None,
    ):
        super().__init__(fonts)
        self.ttc_payload = TtcPayload() if ttc_payload is None else ttc_payload
        self.woff_payload = woff_payload

    def __repr__(self) -> str:
        return object.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SfntFontCollection):
            return False
        return (self.ttc_payload == other.ttc_payload and
                self.woff_payload == other.woff_payload and
                super().__eq__(other))

    def copy(self) -> 'SfntFontCollection':
        fonts = [font.copy() for font in self]
        return SfntFontCollection(
            fonts,
            self.ttc_payload.copy(),
            self.woff_payload.copy(),
        )
