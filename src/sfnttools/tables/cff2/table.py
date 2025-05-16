from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable


class Cff2Table(SfntTable):
    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> Cff2Table:
        # TODO
        return Cff2Table(data)

    data: bytes

    def __init__(self, data: bytes):
        self.data = data

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Cff2Table):
            return False
        return self.data == other.data

    @property
    def num_glyphs(self) -> int:
        # TODO
        return 0

    def calculate_bounds_box(self) -> tuple[int, int, int, int]:
        # TODO
        return 0, 0, 0, 0

    def copy(self) -> Cff2Table:
        # TODO
        return Cff2Table(self.data)

    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        # TODO
        return self.data, {}
