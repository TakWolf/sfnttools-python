from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable
from sfnttools.tables.head.enum import IndexToLocFormat
from sfnttools.tables.head.table import HeadTable
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.utils.stream import Stream


class LocaTable(SfntTable):
    parse_dependencies = ['maxp', 'head']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> LocaTable:
        maxp_table: MaxpTable = tables['maxp']
        head_table: HeadTable = tables['head']

        stream = Stream(data)

        offsets = []
        for _ in range(maxp_table.num_glyphs + 1):
            if head_table.index_to_loc_format == IndexToLocFormat.SHORT:
                offset = stream.read_offset16() * 2
            else:
                offset = stream.read_offset32()
            offsets.append(offset)

        return LocaTable(offsets)

    offsets: list[int]

    def __init__(self, offsets: list[int] | None = None):
        self.offsets = [] if offsets is None else offsets

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LocaTable):
            return False
        return self.offsets == other.offsets

    @property
    def num_offsets(self) -> int:
        return len(self.offsets)

    def copy(self) -> LocaTable:
        return LocaTable(self.offsets.copy())

    def dump_with_index_to_loc_format(self) -> tuple[bytes, IndexToLocFormat]:
        stream = Stream()

        if all(offset % 2 == 0 and offset <= 0xFFFF * 2 for offset in self.offsets):
            index_to_loc_format = IndexToLocFormat.SHORT
        else:
            index_to_loc_format = IndexToLocFormat.LONG

        for offset in self.offsets:
            if index_to_loc_format == IndexToLocFormat.SHORT:
                stream.write_offset16(offset // 2)
            else:
                stream.write_offset32(offset)

        return stream.get_value(), index_to_loc_format

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        head_table: HeadTable = tables['head']

        data, index_to_loc_format = self.dump_with_index_to_loc_format()
        head_table.index_to_loc_format = index_to_loc_format

        return data
