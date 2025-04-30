from sfnttools.table import SfntTableContainer, SfntTable
from sfnttools.utils.stream import Stream


class MaxpTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'MaxpTable':
        stream = Stream(data)

        major_version, minor_version = stream.read_version_16dot16()





        return MaxpTable()

    def __init__(self):
        pass

    def copy(self) -> 'MaxpTable':
        pass

    def dump(self, container: SfntTableContainer) -> bytes:
        pass
