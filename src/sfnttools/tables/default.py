from sfnttools.table import SfntTable


class DefaultTable(SfntTable):
    @staticmethod
    def parse(data: bytes, dependencies: dict[str, SfntTable]) -> 'DefaultTable':
        return DefaultTable(data)

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def copy(self) -> 'DefaultTable':
        return DefaultTable(self.data)

    def dump(self, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        return self.data, {}
