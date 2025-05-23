from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.tables.vhea.table import VheaTable
from sfnttools.tables.vmtx.metric import LongVertMetric
from sfnttools.utils.stream import Stream


class VmtxTable(SfntTable):
    parse_dependencies = ['vhea', 'maxp']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> VmtxTable:
        vhea_table: VheaTable = tables['vhea']
        maxp_table: MaxpTable = tables['maxp']

        stream = Stream(data)

        vert_metrics = []
        for _ in range(vhea_table.num_vert_metrics):
            metric = LongVertMetric.parse(stream)
            vert_metrics.append(metric)

        top_side_bearings = []
        for _ in range(maxp_table.num_glyphs - vhea_table.num_vert_metrics):
            top_side_bearings.append(stream.read_fword())

        return VmtxTable(
            vert_metrics,
            top_side_bearings,
        )

    vert_metrics: list[LongVertMetric]
    top_side_bearings: list[int]

    def __init__(
            self,
            vert_metrics: list[LongVertMetric] | None = None,
            top_side_bearings: list[int] | None = None,
    ):
        self.vert_metrics = [] if vert_metrics is None else vert_metrics
        self.top_side_bearings = [] if top_side_bearings is None else top_side_bearings

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, VmtxTable):
            return False
        return (self.vert_metrics == other.vert_metrics and
                self.top_side_bearings == other.top_side_bearings)

    @property
    def num_vert_metrics(self) -> int:
        return len(self.vert_metrics)

    @property
    def num_top_side_bearings(self) -> int:
        return len(self.top_side_bearings)

    def copy(self) -> SfntTable:
        vert_metrics = [metric.copy() for metric in self.vert_metrics]
        return VmtxTable(
            vert_metrics,
            self.top_side_bearings.copy(),
        )

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        stream = Stream()

        for metric in self.vert_metrics:
            metric.dump(stream)

        for top_side_bearing in self.top_side_bearings:
            stream.write_fword(top_side_bearing)

        return stream.get_value()
