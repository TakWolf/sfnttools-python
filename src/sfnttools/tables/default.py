from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable


class DefaultTable(SfntTable):
    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> DefaultTable:
        return DefaultTable(data)

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DefaultTable):
            return NotImplemented
        return self.data == other.data

    def copy(self) -> DefaultTable:
        return DefaultTable(self.data)

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        return self.data
