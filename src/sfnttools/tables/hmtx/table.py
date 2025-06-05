from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.error import SfntError
from sfnttools.table import SfntTable
from sfnttools.tables.hhea.table import HheaTable
from sfnttools.tables.hmtx.metric import LongHoriMetric
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.utils.stream import Stream


class HmtxTable(SfntTable):
    parse_dependencies = ['maxp', 'hhea']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> HmtxTable:
        maxp_table: MaxpTable = tables['maxp']
        hhea_table: HheaTable = tables['hhea']

        stream = Stream(data)

        hori_metrics = []

        for _ in range(hhea_table.num_hori_metrics):
            metric = LongHoriMetric.parse(stream)
            hori_metrics.append(metric)

        num_additional = maxp_table.num_glyphs - hhea_table.num_hori_metrics
        if num_additional > 0:
            last_metric = hori_metrics[-1]
            for _ in range(num_additional):
                left_side_bearing = stream.read_fword()
                metric = LongHoriMetric(
                    last_metric.advance_width,
                    left_side_bearing,
                )
                hori_metrics.append(metric)

        return HmtxTable(hori_metrics)

    hori_metrics: list[LongHoriMetric]

    def __init__(self, hori_metrics: list[LongHoriMetric] | None = None):
        self.hori_metrics = [] if hori_metrics is None else hori_metrics

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HmtxTable):
            return NotImplemented
        return self.hori_metrics == other.hori_metrics

    def copy(self) -> HmtxTable:
        hori_metrics = [metric.copy() for metric in self.hori_metrics]
        return HmtxTable(hori_metrics)

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        maxp_table: MaxpTable = tables['maxp']
        hhea_table: HheaTable = tables['hhea']

        if len(self.hori_metrics) != maxp_table.num_glyphs:
            raise SfntError('[hmtx] bad number of metrics')

        num_additional = 0
        if len(self.hori_metrics) > 0:
            last_metric = self.hori_metrics[-1]
            for metric in reversed(self.hori_metrics):
                if metric == last_metric:
                    num_additional += 1
                else:
                    break
            num_additional -= 1
        num_hori_metrics = maxp_table.num_glyphs - num_additional

        stream = Stream()

        for i, metric in enumerate(self.hori_metrics):
            if i < num_hori_metrics:
                metric.dump(stream)
            else:
                stream.write_fword(metric.left_side_bearing)

        hhea_table.num_hori_metrics = num_hori_metrics
        return stream.get_value()
