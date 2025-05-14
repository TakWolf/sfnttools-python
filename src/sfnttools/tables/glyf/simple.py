import os
from typing import Any

from sfnttools.error import SfntError
from sfnttools.flags import SfntFlags
from sfnttools.utils.stream import Stream

_SIMPLE_GLYPH_FLAGS_MASK_ON_CURVE_POINT = 0b_0000_0001
_SIMPLE_GLYPH_FLAGS_MASK_X_SHORT_VECTOR = 0b_0000_0010
_SIMPLE_GLYPH_FLAGS_MASK_Y_SHORT_VECTOR = 0b_0000_0100
_SIMPLE_GLYPH_FLAGS_MASK_REPEAT_FLAG = 0b_0000_1000
_SIMPLE_GLYPH_FLAGS_MASK_X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR = 0b_0001_0000
_SIMPLE_GLYPH_FLAGS_MASK_Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR = 0b_0010_0000
_SIMPLE_GLYPH_FLAGS_MASK_OVERLAP_SIMPLE = 0b_0100_0000


class SimpleGlyphFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'SimpleGlyphFlags':
        on_curve_point = value & _SIMPLE_GLYPH_FLAGS_MASK_ON_CURVE_POINT > 0
        x_short_vector = value & _SIMPLE_GLYPH_FLAGS_MASK_X_SHORT_VECTOR > 0
        y_short_vector = value & _SIMPLE_GLYPH_FLAGS_MASK_Y_SHORT_VECTOR > 0
        repeat_flag = value & _SIMPLE_GLYPH_FLAGS_MASK_REPEAT_FLAG > 0
        x_is_same_or_positive_x_short_vector = value & _SIMPLE_GLYPH_FLAGS_MASK_X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR > 0
        y_is_same_or_positive_y_short_vector = value & _SIMPLE_GLYPH_FLAGS_MASK_Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR > 0
        overlap_simple = value & _SIMPLE_GLYPH_FLAGS_MASK_OVERLAP_SIMPLE > 0
        return SimpleGlyphFlags(
            on_curve_point,
            x_short_vector,
            y_short_vector,
            repeat_flag,
            x_is_same_or_positive_x_short_vector,
            y_is_same_or_positive_y_short_vector,
            overlap_simple,
        )

    on_curve_point: bool
    x_short_vector: bool
    y_short_vector: bool
    repeat_flag: bool
    x_is_same_or_positive_x_short_vector: bool
    y_is_same_or_positive_y_short_vector: bool
    overlap_simple: bool

    def __init__(
            self,
            on_curve_point: bool = False,
            x_short_vector: bool = False,
            y_short_vector: bool = False,
            repeat_flag: bool = False,
            x_is_same_or_positive_x_short_vector: bool = False,
            y_is_same_or_positive_y_short_vector: bool = False,
            overlap_simple: bool = False,
    ):
        self.on_curve_point = on_curve_point
        self.x_short_vector = x_short_vector
        self.y_short_vector = y_short_vector
        self.repeat_flag = repeat_flag
        self.x_is_same_or_positive_x_short_vector = x_is_same_or_positive_x_short_vector
        self.y_is_same_or_positive_y_short_vector = y_is_same_or_positive_y_short_vector
        self.overlap_simple = overlap_simple

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SimpleGlyphFlags):
            return False
        return (self.on_curve_point == other.on_curve_point and
                self.x_short_vector == other.x_short_vector and
                self.y_short_vector == other.y_short_vector and
                self.repeat_flag == other.repeat_flag and
                self.x_is_same_or_positive_x_short_vector == other.x_is_same_or_positive_x_short_vector and
                self.y_is_same_or_positive_y_short_vector == other.y_is_same_or_positive_y_short_vector and
                self.overlap_simple == other.overlap_simple)

    @property
    def value(self) -> int:
        value = 0
        if self.on_curve_point:
            value |= _SIMPLE_GLYPH_FLAGS_MASK_ON_CURVE_POINT
        if self.x_short_vector:
            value |= _SIMPLE_GLYPH_FLAGS_MASK_X_SHORT_VECTOR
        if self.y_short_vector:
            value |= _SIMPLE_GLYPH_FLAGS_MASK_Y_SHORT_VECTOR
        if self.repeat_flag:
            value |= _SIMPLE_GLYPH_FLAGS_MASK_REPEAT_FLAG
        if self.x_is_same_or_positive_x_short_vector:
            value |= _SIMPLE_GLYPH_FLAGS_MASK_X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR
        if self.y_is_same_or_positive_y_short_vector:
            value |= _SIMPLE_GLYPH_FLAGS_MASK_Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR
        if self.overlap_simple:
            value |= _SIMPLE_GLYPH_FLAGS_MASK_OVERLAP_SIMPLE
        return value

    def copy(self) -> 'SimpleGlyphFlags':
        return SimpleGlyphFlags(
            self.on_curve_point,
            self.x_short_vector,
            self.y_short_vector,
            self.repeat_flag,
            self.x_is_same_or_positive_x_short_vector,
            self.y_is_same_or_positive_y_short_vector,
            self.overlap_simple,
        )


class GlyphCoordinate:
    @staticmethod
    def calculate_bounds(coordinates: list['GlyphCoordinate']) -> tuple[int, int, int, int]:
        xs = []
        ys = []
        x = 0
        y = 0
        for coordinate in coordinates:
            x += coordinate.delta_x
            y += coordinate.delta_y
            xs.append(x)
            ys.append(y)
        x_min = min(xs, default=0)
        y_min = min(ys, default=0)
        x_max = max(xs, default=0)
        y_max = max(ys, default=0)
        return x_min, y_min, x_max, y_max

    on_curve_point: bool
    delta_x: int
    delta_y: int

    def __init__(
            self,
            on_curve_point: bool = True,
            delta_x: int = 0,
            delta_y: int = 0,
    ):
        self.on_curve_point = on_curve_point
        self.delta_x = delta_x
        self.delta_y = delta_y

    def __repr__(self) -> str:
        return repr((self.delta_x, self.delta_y))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GlyphCoordinate):
            return False
        return (self.on_curve_point == other.on_curve_point and
                self.delta_x == other.delta_x and
                self.delta_y == other.delta_y)

    def copy(self) -> 'GlyphCoordinate':
        return GlyphCoordinate(
            self.on_curve_point,
            self.delta_x,
            self.delta_y,
        )


class SimpleGlyph:
    @staticmethod
    def parse_body(
            stream: Stream,
            num_contours: int,
            x_min: int,
            y_min: int,
            x_max: int,
            y_max: int,
    ) -> 'SimpleGlyph':
        end_pts_of_contours = [stream.read_uint16() for _ in range(num_contours)]
        num_coordinates = end_pts_of_contours[-1] + 1
        instruction_length = stream.read_uint16()
        instructions = stream.read(instruction_length)

        flags_list = []
        while len(flags_list) < num_coordinates:
            flags = SimpleGlyphFlags.parse(stream.read_uint8())
            if flags.repeat_flag:
                additional_repeat_times = stream.read_uint8()
            else:
                additional_repeat_times = 0
            for _ in range(additional_repeat_times + 1):
                flags_list.append(flags)
        if len(flags_list) != num_coordinates:
            raise SfntError('[glyf] bad number of coordinates')

        x_coordinates = []
        for flags in flags_list:
            if flags.x_short_vector:
                delta_x = stream.read_uint8()
                if not flags.x_is_same_or_positive_x_short_vector:
                    delta_x *= -1
            elif flags.x_is_same_or_positive_x_short_vector:
                delta_x = 0
            else:
                delta_x = stream.read_int16()
            x_coordinates.append(delta_x)

        y_coordinates = []
        for flags in flags_list:
            if flags.y_short_vector:
                delta_y = stream.read_uint8()
                if not flags.y_is_same_or_positive_y_short_vector:
                    delta_y *= -1
            elif flags.y_is_same_or_positive_y_short_vector:
                delta_y = 0
            else:
                delta_y = stream.read_int16()
            y_coordinates.append(delta_y)

        coordinates = []
        for flags, (delta_x, delta_y) in zip(flags_list, zip(x_coordinates, y_coordinates)):
            coordinates.append(GlyphCoordinate(flags.on_curve_point, delta_x, delta_y))

        return SimpleGlyph(
            x_min,
            y_min,
            x_max,
            y_max,
            end_pts_of_contours,
            coordinates,
            instructions,
            flags_list[0].overlap_simple,
        )

    @staticmethod
    def parse(data: bytes) -> 'SimpleGlyph':
        stream = Stream(data)

        num_contours = stream.read_int16()
        x_min = stream.read_int16()
        y_min = stream.read_int16()
        x_max = stream.read_int16()
        y_max = stream.read_int16()

        return SimpleGlyph.parse_body(stream, num_contours, x_min, y_min, x_max, y_max)

    x_min: int
    y_min: int
    x_max: int
    y_max: int
    end_pts_of_contours: list[int]
    coordinates: list[GlyphCoordinate]
    instructions: bytes
    overlap_simple: bool

    def __init__(
            self,
            x_min: int = 0,
            y_min: int = 0,
            x_max: int = 0,
            y_max: int = 0,
            end_pts_of_contours: list[int] | None = None,
            coordinates: list[GlyphCoordinate] | None = None,
            instructions: bytes = b'',
            overlap_simple: bool = False,
    ):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.end_pts_of_contours = [] if end_pts_of_contours is None else end_pts_of_contours
        self.coordinates = [] if coordinates is None else coordinates
        self.instructions = instructions
        self.overlap_simple = overlap_simple

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SimpleGlyph):
            return False
        return (self.x_min == other.x_min and
                self.y_min == other.y_min and
                self.x_max == other.x_max and
                self.y_max == other.y_max and
                self.end_pts_of_contours == other.end_pts_of_contours and
                self.coordinates == other.coordinates and
                self.instructions == other.instructions and
                self.overlap_simple == other.overlap_simple)

    @property
    def num_contours(self) -> int:
        return len(self.end_pts_of_contours)

    def copy(self) -> 'SimpleGlyph':
        return SimpleGlyph(
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
            self.end_pts_of_contours.copy(),
            [coordinate.copy() for coordinate in self.coordinates],
            self.instructions,
            self.overlap_simple,
        )

    def dump_body(self, stream: Stream):
        if len(self.coordinates) != self.end_pts_of_contours[-1] + 1:
            raise SfntError('[glyf] bad number of coordinates')

        flags_stream = Stream()
        x_stream = Stream()
        y_stream = Stream()
        last_flags_value = None
        additional_repeat_times = 0
        for i, coordinate in enumerate(self.coordinates):
            flags = SimpleGlyphFlags(
                on_curve_point=coordinate.on_curve_point,
            )

            if i == 0:
                flags.overlap_simple = self.overlap_simple

            if coordinate.delta_x == 0:
                flags.x_is_same_or_positive_x_short_vector = True
            elif -0xFF <= coordinate.delta_x <= 0xFF:
                flags.x_short_vector = True
                if coordinate.delta_x > 0:
                    flags.x_is_same_or_positive_x_short_vector = True
                x_stream.write_uint8(abs(coordinate.delta_x))
            else:
                x_stream.write_int16(coordinate.delta_x)

            if coordinate.delta_y == 0:
                flags.y_is_same_or_positive_y_short_vector = True
            elif -0xFF <= coordinate.delta_y <= 0xFF:
                flags.y_short_vector = True
                if coordinate.delta_y > 0:
                    flags.y_is_same_or_positive_y_short_vector = True
                y_stream.write_uint8(abs(coordinate.delta_y))
            else:
                y_stream.write_int16(coordinate.delta_y)

            flags_value = flags.value
            if flags_value == last_flags_value and additional_repeat_times < 0xFF:
                additional_repeat_times += 1
                if additional_repeat_times == 1:
                    flags_stream.write_uint8(flags_value)
                else:
                    flags_stream.seek(-2, os.SEEK_CUR)
                    flags_stream.write_uint8(flags_value | _SIMPLE_GLYPH_FLAGS_MASK_REPEAT_FLAG)
                    flags_stream.write_uint8(additional_repeat_times)
            else:
                additional_repeat_times = 0
                flags_stream.write_uint8(flags_value)
            last_flags_value = flags_value

        for index in self.end_pts_of_contours:
            stream.write_uint16(index)
        stream.write_uint16(len(self.instructions))
        stream.write(self.instructions)

        stream.write(flags_stream.get_value())
        stream.write(x_stream.get_value())
        stream.write(y_stream.get_value())

    def dump(self) -> bytes:
        stream = Stream()

        stream.write_int16(self.num_contours)
        stream.write_int16(self.x_min)
        stream.write_int16(self.y_min)
        stream.write_int16(self.x_max)
        stream.write_int16(self.y_max)

        self.dump_body(stream)

        return stream.get_value()
