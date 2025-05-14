from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable


class DefaultTable(SfntTable):
    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> 'DefaultTable':
        return DefaultTable(data)

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DefaultTable):
            return False
        return self.data == other.data

    def copy(self) -> 'DefaultTable':
        return DefaultTable(self.data)

    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        return self.data, {}
