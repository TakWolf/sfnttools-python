from sfnttools.table import SfntTableContainer, SfntTable
from sfnttools.tables.head import HeadTable
from sfnttools.tables.maxp import MaxpTable
from sfnttools.utils.stream import Stream


class LocaTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'LocaTable':
        head_table: HeadTable = container.get_table('head')
        maxp_table: MaxpTable = container.get_table('maxp')
        stream = Stream(data)






        return LocaTable()

    def __init__(self):
        pass

    def copy(self) -> 'LocaTable':
        pass

    def dump(self, container: SfntTableContainer) -> bytes:
        pass
