from __future__ import annotations

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable


class VmtxTable(SfntTable):
    parse_dependencies = ['vhea', 'maxp']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> VmtxTable:
        pass




    def copy(self) -> SfntTable:
        pass

    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        pass