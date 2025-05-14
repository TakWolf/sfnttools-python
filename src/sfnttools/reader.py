from abc import abstractmethod
from collections.abc import Iterator

from sfnttools.configs import SfntConfigs
from sfnttools.error import SfntError
from sfnttools.payload import TtcPayload, WoffPayload
from sfnttools.table import SfntTable
from sfnttools.tag import SfntVersion
from sfnttools.utils.checksum import calculate_checksum, calculate_checksum_adjustment


class SfntReader:
    configs: SfntConfigs
    share_tables: bool
    verify_checksum: bool
    tables_cache: dict[str, tuple[SfntTable, int]]

    def __init__(
            self,
            configs: SfntConfigs,
            share_tables: bool,
            verify_checksum: bool,
    ):
        self.configs = configs
        self.share_tables = share_tables
        self.verify_checksum = verify_checksum
        self.tables_cache = {}

    @abstractmethod
    def is_font_collection(self) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_sfnt_version(self) -> SfntVersion:
        raise NotImplementedError()

    @abstractmethod
    def get_table_tags(self) -> Iterator[str]:
        raise NotImplementedError()

    @abstractmethod
    def reconstruct_header_data(self) -> bytes:
        raise NotImplementedError()

    @abstractmethod
    def read_table_data_and_expected_checksum(self, tag: str) -> tuple[bytes, int | None]:
        raise NotImplementedError()

    @abstractmethod
    def get_table_and_checksum_from_collection_cache(self, tag: str) -> tuple[SfntTable, int] | None:
        raise NotImplementedError()

    @abstractmethod
    def set_table_and_checksum_to_collection_cache(self, tag: str, table: SfntTable, checksum: int):
        raise NotImplementedError()

    @abstractmethod
    def read_woff_payload(self) -> WoffPayload | None:
        raise NotImplementedError()

    def get_or_parse_table(self, tag: str) -> SfntTable:
        table, checksum = self.tables_cache.get(tag, (None, None))

        if table is None and self.is_font_collection():
            table, checksum = self.get_table_and_checksum_from_collection_cache(tag) or (None, None)
            if table is not None:
                if not self.share_tables:
                    table = table.copy()
                self.tables_cache[tag] = table, checksum

        if table is None:
            data, expected_checksum = self.read_table_data_and_expected_checksum(tag)
            if self.verify_checksum:
                if tag == 'head':
                    checksum = calculate_checksum(data[:8] + b'\x00\x00\x00\x00' + data[12:])
                else:
                    checksum = calculate_checksum(data)
            else:
                checksum = 0

            if self.verify_checksum and expected_checksum is not None and checksum != expected_checksum:
                raise SfntError(f'table {repr(tag)} bad checksum')

            from sfnttools.tables.factory import TABLE_TYPE_REGISTRY, DEFAULT_TABLE_TYPE
            table_type = TABLE_TYPE_REGISTRY.get(tag, DEFAULT_TABLE_TYPE)

            dependencies = {}
            for dependency_tag in table_type.parse_dependencies:
                dependency_table = self.get_or_parse_table(dependency_tag)
                dependencies[dependency_tag] = dependency_table

            table = table_type.parse(data, self.configs, dependencies)
            self.tables_cache[tag] = table, checksum
            if self.is_font_collection():
                self.set_table_and_checksum_to_collection_cache(tag, table, checksum)

        return table

    def parse_font(self) -> tuple[SfntVersion, dict[str, SfntTable]]:
        tables = {}
        for tag in self.get_table_tags():
            if tag in tables:
                raise SfntError(f'table {repr(tag)} duplicate')
            table = self.get_or_parse_table(tag)
            tables[tag] = table

        if self.verify_checksum and not self.is_font_collection() and 'head' in self.tables_cache:
            checksums = [calculate_checksum(self.reconstruct_header_data())]
            for _, checksum in self.tables_cache.values():
                checksums.append(checksum)
            checksum_adjustment = calculate_checksum_adjustment(checksums)
            if checksum_adjustment != self.tables_cache['head'][0].checksum_adjustment:
                raise SfntError(f'bad checksum adjustment')

        return self.get_sfnt_version(), tables


class SfntCollectionReader:
    @property
    @abstractmethod
    def num_fonts(self) -> int:
        raise NotImplementedError()

    @abstractmethod
    def create_reader(self, font_index: int) -> SfntReader:
        raise NotImplementedError()

    @abstractmethod
    def read_ttc_payload(self) -> TtcPayload:
        raise NotImplementedError()

    @abstractmethod
    def read_woff_payload(self) -> WoffPayload | None:
        raise NotImplementedError()
