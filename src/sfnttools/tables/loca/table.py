from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable
from sfnttools.tables.head.enum import IndexToLocFormat
from sfnttools.tables.head.table import HeadTable
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.utils.stream import Stream


class LocaTable(SfntTable):
    parse_dependencies = ['maxp', 'head']
    dump_dependencies = ['head']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> 'LocaTable':
        maxp_table: MaxpTable = dependencies['maxp']
        head_table: HeadTable = dependencies['head']

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

    def copy(self) -> 'LocaTable':
        return LocaTable(self.offsets.copy())

    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        head_table: HeadTable = dependencies['head']

        max_offset = max(self.offsets, default=0)
        if max_offset <= 0xFFFF * 2 and all(offset % 2 == 0 for offset in self.offsets):
            head_table.index_to_loc_format = IndexToLocFormat.SHORT
        else:
            head_table.index_to_loc_format = IndexToLocFormat.LONG

        stream = Stream()

        for offset in self.offsets:
            if head_table.index_to_loc_format == IndexToLocFormat.SHORT:
                stream.write_offset16(offset // 2)
            else:
                stream.write_offset32(offset)

        return stream.get_value(), {}
