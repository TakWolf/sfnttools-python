from __future__ import annotations

from typing import Any

from sfnttools.flags import SfntFlags
from sfnttools.tables.hhea.table import HheaTable
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.utils.stream import Stream

_OPTION_FLAGS_MASK_HAS_PROPORTIONAL_LEFT_SIDE_BEARINGS = 0b_0000_0000_0000_0001
_OPTION_FLAGS_MASK_HAS_MONOSPACED_LEFT_SIDE_BEARINGS = 0b_0000_0000_0000_0010


class OptionFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> OptionFlags:
        has_proportional_left_side_bearings = value & _OPTION_FLAGS_MASK_HAS_PROPORTIONAL_LEFT_SIDE_BEARINGS > 0
        has_monospaced_left_side_bearings = value & _OPTION_FLAGS_MASK_HAS_MONOSPACED_LEFT_SIDE_BEARINGS > 0
        return OptionFlags(
            has_proportional_left_side_bearings,
            has_monospaced_left_side_bearings,
        )

    has_proportional_left_side_bearings: bool
    has_monospaced_left_side_bearings: bool

    def __init__(
            self,
            has_proportional_left_side_bearings: bool = False,
            has_monospaced_left_side_bearings: bool = False,
    ):
        self.has_proportional_left_side_bearings = has_proportional_left_side_bearings
        self.has_monospaced_left_side_bearings = has_monospaced_left_side_bearings

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, OptionFlags):
            return NotImplemented
        return (self.has_proportional_left_side_bearings == other.has_proportional_left_side_bearings and
                self.has_monospaced_left_side_bearings == other.has_monospaced_left_side_bearings)

    @property
    def value(self) -> int:
        value = 0
        if self.has_proportional_left_side_bearings:
            value |= _OPTION_FLAGS_MASK_HAS_PROPORTIONAL_LEFT_SIDE_BEARINGS
        if self.has_monospaced_left_side_bearings:
            value |= _OPTION_FLAGS_MASK_HAS_MONOSPACED_LEFT_SIDE_BEARINGS
        return value

    def copy(self) -> OptionFlags:
        return OptionFlags(
            self.has_proportional_left_side_bearings,
            self.has_monospaced_left_side_bearings,
        )


class TransformedHmtxTable:
    @staticmethod
    def parse(data: bytes, maxp_table: MaxpTable, hhea_table: HheaTable) -> TransformedHmtxTable:
        stream = Stream(data)

        option_flags = OptionFlags.parse(stream.read_uint8())

        advance_widths = [stream.read_uint16() for _ in range(hhea_table.num_hori_metrics)]

        if option_flags.has_proportional_left_side_bearings:
            proportional_left_side_bearings = [stream.read_int16() for _ in range(hhea_table.num_hori_metrics)]
        else:
            proportional_left_side_bearings = []

        if option_flags.has_monospaced_left_side_bearings:
            monospaced_left_side_bearings = [stream.read_int16() for _ in range(maxp_table.num_glyphs - hhea_table.num_hori_metrics)]
        else:
            monospaced_left_side_bearings = []

        return TransformedHmtxTable(
            advance_widths,
            proportional_left_side_bearings,
            monospaced_left_side_bearings,
        )

    advance_widths: list[int]
    proportional_left_side_bearings: list[int]
    monospaced_left_side_bearings: list[int]

    def __init__(
            self,
            advance_widths: list[int] | None = None,
            proportional_left_side_bearings: list[int] | None = None,
            monospaced_left_side_bearings: list[int] | None = None,
    ):
        self.advance_widths = advance_widths
        self.proportional_left_side_bearings = proportional_left_side_bearings
        self.monospaced_left_side_bearings = monospaced_left_side_bearings








    def dump(self) -> bytes:
        option_flags = OptionFlags(
            has_proportional_left_side_bearings=len(self.proportional_left_side_bearings) > 0,
            has_monospaced_left_side_bearings=len(self.monospaced_left_side_bearings) > 0,
        )

        stream = Stream()

        stream.write_uint8(option_flags.value)

        for advance_width in self.advance_widths:
            stream.write_int16(advance_width)

        for left_side_bearing in self.proportional_left_side_bearings:
            stream.write_int16(left_side_bearing)

        for left_side_bearing in self.monospaced_left_side_bearings:
            stream.write_int16(left_side_bearing)

        return stream.get_value()
