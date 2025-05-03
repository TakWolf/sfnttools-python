from io import BytesIO

from sfnttools.error import SfntError
from sfnttools.table import SfntTableContainer, SfntTable
from sfnttools.tables.head import HeadTable, IndexToLocFormat
from sfnttools.tables.maxp import MaxpTable
from sfnttools.utils.stream import Stream


class LocaTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'LocaTable':
        maxp_table: MaxpTable = container.get_table('maxp')
        head_table: HeadTable = container.get_table('head')

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

    def copy(self) -> 'LocaTable':
        return LocaTable(self.offsets.copy())

    def dump(self, container: SfntTableContainer) -> bytes:
        maxp_table: MaxpTable = container.get_table('maxp')
        head_table: HeadTable = container.get_table('head')

        if len(self.offsets) - 1 != maxp_table.num_glyphs:
            raise SfntError('[loca] bad offsets length')

        buffer = BytesIO()
        stream = Stream(buffer)

        for offset in self.offsets:
            if head_table.index_to_loc_format == IndexToLocFormat.SHORT:
                stream.write_offset16(offset // 2)
            else:
                stream.write_offset32(offset)

        return buffer.getvalue()
