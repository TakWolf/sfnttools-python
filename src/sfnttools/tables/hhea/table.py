from __future__ import annotations

from typing import Any, TYPE_CHECKING

from sfnttools.configs import SfntConfigs
from sfnttools.table import SfntTable
from sfnttools.tables.hhea.enum import MetricDataFormat
from sfnttools.utils.stream import Stream

if TYPE_CHECKING:
    from sfnttools.tables.hmtx.table import HmtxTable


class HheaTable(SfntTable):
    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, tables: dict[str, SfntTable]) -> HheaTable:
        stream = Stream(data)

        major_version = stream.read_uint16()
        minor_version = stream.read_uint16()
        ascender = stream.read_fword()
        descender = stream.read_fword()
        line_gap = stream.read_fword()
        advance_width_max = stream.read_ufword()
        min_left_side_bearing = stream.read_fword()
        min_right_side_bearing = stream.read_fword()
        x_max_extent = stream.read_fword()
        caret_slope_rise = stream.read_int16()
        caret_slope_run = stream.read_int16()
        caret_offset = stream.read_int16()
        stream.read_int16()
        stream.read_int16()
        stream.read_int16()
        stream.read_int16()
        metric_data_format = MetricDataFormat(stream.read_int16())
        num_hori_metrics = stream.read_uint16()

        return HheaTable(
            major_version,
            minor_version,
            ascender,
            descender,
            line_gap,
            advance_width_max,
            min_left_side_bearing,
            min_right_side_bearing,
            x_max_extent,
            caret_slope_rise,
            caret_slope_run,
            caret_offset,
            metric_data_format,
            num_hori_metrics,
        )

    major_version: int
    minor_version: int
    ascender: int
    descender: int
    line_gap: int
    advance_width_max: int
    min_left_side_bearing: int
    min_right_side_bearing: int
    x_max_extent: int
    caret_slope_rise: int
    caret_slope_run: int
    caret_offset: int
    metric_data_format: MetricDataFormat
    num_hori_metrics: int

    def __init__(
            self,
            major_version: int = 1,
            minor_version: int = 0,
            ascender: int = 0,
            descender: int = 0,
            line_gap: int = 0,
            advance_width_max: int = 0,
            min_left_side_bearing: int = 0,
            min_right_side_bearing: int = 0,
            x_max_extent: int = 0,
            caret_slope_rise: int = 1,
            caret_slope_run: int = 0,
            caret_offset: int = 0,
            metric_data_format: MetricDataFormat = MetricDataFormat.CURRENT,
            num_hori_metrics: int = 0,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.ascender = ascender
        self.descender = descender
        self.line_gap = line_gap
        self.advance_width_max = advance_width_max
        self.min_left_side_bearing = min_left_side_bearing
        self.min_right_side_bearing = min_right_side_bearing
        self.x_max_extent = x_max_extent
        self.caret_slope_rise = caret_slope_rise
        self.caret_slope_run = caret_slope_run
        self.caret_offset = caret_offset
        self.metric_data_format = metric_data_format
        self.num_hori_metrics = num_hori_metrics

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HheaTable):
            return False
        return (self.major_version == other.major_version and
                self.minor_version == other. minor_version and
                self.ascender == other. ascender and
                self.descender == other. descender and
                self.line_gap == other. line_gap and
                self.advance_width_max == other. advance_width_max and
                self.min_left_side_bearing == other. min_left_side_bearing and
                self.min_right_side_bearing == other. min_right_side_bearing and
                self.x_max_extent == other. x_max_extent and
                self.caret_slope_rise == other. caret_slope_rise and
                self.caret_slope_run == other. caret_slope_run and
                self.caret_offset == other. caret_offset and
                self.metric_data_format == other. metric_data_format and
                self.num_hori_metrics == other. num_hori_metrics)

    def copy(self) -> HheaTable:
        return HheaTable(
            self.major_version,
            self.minor_version,
            self.ascender,
            self.descender,
            self.line_gap,
            self.advance_width_max,
            self.min_left_side_bearing,
            self.min_right_side_bearing,
            self.x_max_extent,
            self.caret_slope_rise,
            self.caret_slope_run,
            self.caret_offset,
            self.metric_data_format,
            self.num_hori_metrics,
        )

    def update(self, configs: SfntConfigs, tables: dict[str, SfntTable]):
        hmtx_table: HmtxTable = tables['hmtx']

        self.advance_width_max = max(metric.advance_width for metric in hmtx_table.hori_metrics)

        # TODO

    def dump(self, configs: SfntConfigs, tables: dict[str, SfntTable]) -> bytes:
        stream = Stream()

        stream.write_uint16(self.major_version)
        stream.write_uint16(self.minor_version)
        stream.write_fword(self.ascender)
        stream.write_fword(self.descender)
        stream.write_fword(self.line_gap)
        stream.write_ufword(self.advance_width_max)
        stream.write_fword(self.min_left_side_bearing)
        stream.write_fword(self.min_right_side_bearing)
        stream.write_fword(self.x_max_extent)
        stream.write_int16(self.caret_slope_rise)
        stream.write_int16(self.caret_slope_run)
        stream.write_int16(self.caret_offset)
        stream.write_int16(0)
        stream.write_int16(0)
        stream.write_int16(0)
        stream.write_int16(0)
        stream.write_int16(self.metric_data_format)
        stream.write_uint16(self.num_hori_metrics)

        return stream.get_value()
