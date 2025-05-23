from __future__ import annotations

from typing import Any

from sfnttools.configs import SfntConfigs
from sfnttools.error import SfntError
from sfnttools.table import SfntTable
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.tables.vhea.table import VheaTable
from sfnttools.tables.vmtx.metric import LongVertMetric
from sfnttools.utils.stream import Stream


class VmtxTable(SfntTable):
    parse_dependencies = ['maxp', 'vhea']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> VmtxTable:
        maxp_table: MaxpTable = tables['maxp']
        vhea_table: VheaTable = tables['vhea']

        stream = Stream(data)

        vert_metrics = []

        for _ in range(vhea_table.num_vert_metrics):
            metric = LongVertMetric.parse(stream)
            vert_metrics.append(metric)

        num_additional = maxp_table.num_glyphs - vhea_table.num_vert_metrics
        if num_additional > 0:
            last_metric = vert_metrics[-1]
            for _ in range(num_additional):
                top_side_bearing = stream.read_fword()
                metric = LongVertMetric(
                    last_metric.advance_height,
                    top_side_bearing,
                )
                vert_metrics.append(metric)

        return VmtxTable(vert_metrics)

    vert_metrics: list[LongVertMetric]

    def __init__(self, vert_metrics: list[LongVertMetric] | None = None):
        self.vert_metrics = [] if vert_metrics is None else vert_metrics

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, VmtxTable):
            return False
        return self.vert_metrics == other.vert_metrics

    def copy(self) -> SfntTable:
        vert_metrics = [metric.copy() for metric in self.vert_metrics]
        return VmtxTable(vert_metrics)

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        maxp_table: MaxpTable = tables['maxp']
        vhea_table: VheaTable = tables['vhea']

        if len(self.vert_metrics) != maxp_table.num_glyphs:
            raise SfntError('[vmtx] bad number of metrics')

        num_additional = 0
        if len(self.vert_metrics) > 0:
            last_metric = self.vert_metrics[-1]
            for metric in reversed(self.vert_metrics):
                if metric == last_metric:
                    num_additional += 1
                else:
                    break
            num_additional -= 1
        num_vert_metrics = maxp_table.num_glyphs - num_additional

        stream = Stream()

        for i, metric in enumerate(self.vert_metrics):
            if i < num_vert_metrics:
                metric.dump(stream)
            else:
                stream.write_fword(metric.top_side_bearing)

        vhea_table.num_vert_metrics = num_vert_metrics
        return stream.get_value()
