from sfnttools.table import SfntTable, SfntTableContainer


class DefaultTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'DefaultTable':
        return DefaultTable(data)

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def copy(self) -> 'DefaultTable':
        return DefaultTable(self.data)

    def dump(self, container: SfntTableContainer) -> bytes:
        return self.data
