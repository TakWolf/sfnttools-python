from __future__ import annotations

from typing import Any

from sfnttools.utils.stream import Stream


class LongVertMetric:
    @staticmethod
    def parse(stream: Stream) -> LongVertMetric:
        advance_height = stream.read_ufword()
        top_side_bearing = stream.read_fword()
        return LongVertMetric(
            advance_height,
            top_side_bearing,
        )

    advance_height: int
    top_side_bearing: int

    def __init__(
            self,
            advance_height: int,
            top_side_bearing: int,
    ):
        self.advance_height = advance_height
        self.top_side_bearing = top_side_bearing

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, LongVertMetric):
            return False
        return (self.advance_height == other.advance_height and
                self.top_side_bearing == other.top_side_bearing)

    def copy(self) -> LongVertMetric:
        return LongVertMetric(
            self.advance_height,
            self.top_side_bearing,
        )

    def dump(self, stream: Stream):
        stream.write_ufword(self.advance_height)
        stream.write_fword(self.top_side_bearing)
