from sfnttools.table import SfntTableContainer, SfntTable


class LocaTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'LocaTable':
        pass

    def copy(self) -> 'LocaTable':
        pass

    def dump(self, container: SfntTableContainer) -> bytes:
        pass
