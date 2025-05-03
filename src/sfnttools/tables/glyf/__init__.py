from io import BytesIO

from sfnttools.table import SfntTableContainer, SfntTable
from sfnttools.utils.stream import Stream


class GlyfTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'GlyfTable':
        stream = Stream(data)

        # TODO

        return GlyfTable()

    def __init__(self):
        pass

    def copy(self) -> 'GlyfTable':
        return GlyfTable()

    def dump(self, container: SfntTableContainer) -> bytes:
        buffer = BytesIO()
        stream = Stream(buffer)

        # TODO

        return buffer.getvalue()
