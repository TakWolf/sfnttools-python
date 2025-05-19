from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable
from sfnttools.utils.stream import Stream


class HmtxTable(SfntTable):
    parse_dependencies = ['hhea', 'maxp']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> HmtxTable:
        from sfnttools.tables.hhea.table import HheaTable
        hhea_table: HheaTable = dependencies['hhea']
        from sfnttools.tables.maxp.table import MaxpTable
        maxp_table: MaxpTable = dependencies['maxp']

        stream = Stream(data)

        h_metrics = []
        for _ in range(hhea_table.num_h_metrics):
            metric = LongHorMetric.parse(stream)
            h_metrics.append(metric)

        left_side_bearings = []
        for _ in range(maxp_table.num_glyphs - hhea_table.num_h_metrics):
            left_side_bearings.append(stream.read_fword())

        return HmtxTable(
            h_metrics,
            left_side_bearings,
        )

    h_metrics: list[LongHorMetric]
    left_side_bearings: list[int]

    def __init__(
            self,
            h_metrics: list[LongHorMetric] | None = None,
            left_side_bearings: list[int] | None = None,
    ):
        self.h_metrics = [] if h_metrics is None else h_metrics
        self.left_side_bearings = [] if left_side_bearings is None else left_side_bearings

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HmtxTable):
            return False
        return (self.h_metrics == other.h_metrics and
                self.left_side_bearings == other.left_side_bearings)

    @property
    def num_h_metrics(self) -> int:
        return len(self.h_metrics)

    @property
    def num_left_side_bearings(self) -> int:
        return len(self.left_side_bearings)

    def copy(self) -> HmtxTable:
        h_metrics = [metric.copy() for metric in self.h_metrics]
        return HmtxTable(
            h_metrics,
            self.left_side_bearings.copy(),
        )

    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        stream = Stream()

        for metrics in self.h_metrics:
            metrics.dump(stream)

        for left_side_bearing in self.left_side_bearings:
            stream.write_fword(left_side_bearing)

        return stream.get_value(), {}
