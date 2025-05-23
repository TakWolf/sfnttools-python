from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable
from sfnttools.tables.hhea.table import HheaTable
from sfnttools.tables.hmtx.metric import LongHoriMetric
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.utils.stream import Stream


class HmtxTable(SfntTable):
    parse_dependencies = ['hhea', 'maxp']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> HmtxTable:
        hhea_table: HheaTable = tables['hhea']
        maxp_table: MaxpTable = tables['maxp']

        stream = Stream(data)

        hori_metrics = []
        for _ in range(hhea_table.num_hori_metrics):
            metric = LongHoriMetric.parse(stream)
            hori_metrics.append(metric)

        left_side_bearings = []
        for _ in range(maxp_table.num_glyphs - hhea_table.num_hori_metrics):
            left_side_bearings.append(stream.read_fword())

        return HmtxTable(
            hori_metrics,
            left_side_bearings,
        )

    hori_metrics: list[LongHoriMetric]
    left_side_bearings: list[int]

    def __init__(
            self,
            hori_metrics: list[LongHoriMetric] | None = None,
            left_side_bearings: list[int] | None = None,
    ):
        self.hori_metrics = [] if hori_metrics is None else hori_metrics
        self.left_side_bearings = [] if left_side_bearings is None else left_side_bearings

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HmtxTable):
            return False
        return (self.hori_metrics == other.hori_metrics and
                self.left_side_bearings == other.left_side_bearings)

    @property
    def num_hori_metrics(self) -> int:
        return len(self.hori_metrics)

    @property
    def num_left_side_bearings(self) -> int:
        return len(self.left_side_bearings)

    def copy(self) -> HmtxTable:
        hori_metrics = [metric.copy() for metric in self.hori_metrics]
        return HmtxTable(
            hori_metrics,
            self.left_side_bearings.copy(),
        )

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        stream = Stream()

        for metric in self.hori_metrics:
            metric.dump(stream)

        for left_side_bearing in self.left_side_bearings:
            stream.write_fword(left_side_bearing)

        return stream.get_value()
