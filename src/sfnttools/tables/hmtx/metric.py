from __future__ import annotations

from typing import Any

from sfnttools.utils.stream import Stream


class LongHoriMetric:
    @staticmethod
    def parse(stream: Stream) -> LongHoriMetric:
        advance_width = stream.read_ufword()
        left_side_bearing = stream.read_fword()
        return LongHoriMetric(
            advance_width,
            left_side_bearing,
        )

    advance_width: int
    left_side_bearing: int

    def __init__(
            self,
            advance_width: int,
            left_side_bearing: int,
    ):
        self.advance_width = advance_width
        self.left_side_bearing = left_side_bearing

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LongHoriMetric):
            return NotImplemented
        return (self.advance_width == other.advance_width and
                self.left_side_bearing == other.left_side_bearing)

    def copy(self) -> LongHoriMetric:
        return LongHoriMetric(
            self.advance_width,
            self.left_side_bearing,
        )

    def dump(self, stream: Stream):
        stream.write_ufword(self.advance_width)
        stream.write_fword(self.left_side_bearing)
