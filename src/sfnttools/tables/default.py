from sfnttools.table import SfntTableReader, SfntTableWriter, SfntTable


class DefaultTable(SfntTable):
    @staticmethod
    def parse(data: bytes, reader: SfntTableReader) -> 'DefaultTable':
        return DefaultTable(data)

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def copy(self) -> 'DefaultTable':
        return DefaultTable(self.data)

    def dump(self, writer: SfntTableWriter) -> bytes:
        return self.data
