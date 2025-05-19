from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable


class CffTable(SfntTable):
    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> CffTable:
        # TODO
        return CffTable(data)

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CffTable):
            return False
        return self.data == other.data

    @property
    def num_glyphs(self) -> int:
        # TODO
        return 0

    def calculate_bounds_box(self) -> tuple[int, int, int, int]:
        # TODO
        return 0, 0, 0, 0

    def copy(self) -> CffTable:
        # TODO
        return CffTable(self.data)

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        # TODO
        return self.data, {}
