from typing import Final

from sfnttools.error import SfntError
from sfnttools.table import SfntFlags
from sfnttools.tables.glyf.description import GlyphDescription
from sfnttools.utils.stream import Stream

SIMPLE_GLYPH_FLAGS_MASK_ON_CURVE_POINT: Final = 0b_0000_0001
SIMPLE_GLYPH_FLAGS_MASK_X_SHORT_VECTOR: Final = 0b_0000_0010
SIMPLE_GLYPH_FLAGS_MASK_Y_SHORT_VECTOR: Final = 0b_0000_0100
SIMPLE_GLYPH_FLAGS_MASK_REPEAT_FLAG: Final = 0b_0000_1000
SIMPLE_GLYPH_FLAGS_MASK_X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR: Final = 0b_0001_0000
SIMPLE_GLYPH_FLAGS_MASK_Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR: Final = 0b_0010_0000
SIMPLE_GLYPH_FLAGS_MASK_OVERLAP_SIMPLE: Final = 0b_0100_0000


class SimpleGlyphFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'SimpleGlyphFlags':
        on_curve_point = value & SIMPLE_GLYPH_FLAGS_MASK_ON_CURVE_POINT > 0
        x_short_vector = value & SIMPLE_GLYPH_FLAGS_MASK_X_SHORT_VECTOR > 0
        y_short_vector = value & SIMPLE_GLYPH_FLAGS_MASK_Y_SHORT_VECTOR > 0
        repeat_flag = value & SIMPLE_GLYPH_FLAGS_MASK_REPEAT_FLAG > 0
        x_is_same_or_positive_x_short_vector = value & SIMPLE_GLYPH_FLAGS_MASK_X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR > 0
        y_is_same_or_positive_y_short_vector = value & SIMPLE_GLYPH_FLAGS_MASK_Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR > 0
        overlap_simple = value & SIMPLE_GLYPH_FLAGS_MASK_OVERLAP_SIMPLE > 0
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

    @property
    def value(self) -> int:
        value = 0
        if self.on_curve_point:
            value |= SIMPLE_GLYPH_FLAGS_MASK_ON_CURVE_POINT
        if self.x_short_vector:
            value |= SIMPLE_GLYPH_FLAGS_MASK_X_SHORT_VECTOR
        if self.y_short_vector:
            value |= SIMPLE_GLYPH_FLAGS_MASK_Y_SHORT_VECTOR
        if self.repeat_flag:
            value |= SIMPLE_GLYPH_FLAGS_MASK_REPEAT_FLAG
        if self.x_is_same_or_positive_x_short_vector:
            value |= SIMPLE_GLYPH_FLAGS_MASK_X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR
        if self.y_is_same_or_positive_y_short_vector:
            value |= SIMPLE_GLYPH_FLAGS_MASK_Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR
        if self.overlap_simple:
            value |= SIMPLE_GLYPH_FLAGS_MASK_OVERLAP_SIMPLE
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
    x: int
    y: int
    on_curve_point: bool

    def __init__(self, x: int, y: int, on_curve_point: bool):
        self.x = x
        self.y = y
        self.on_curve_point = on_curve_point

    def __repr__(self) -> str:
        return repr((self.x, self.y))

    def copy(self) -> 'GlyphCoordinate':
        return GlyphCoordinate(self.x, self.y, self.on_curve_point)


class SimpleGlyphTable(GlyphDescription):
    @staticmethod
    def parse(stream: Stream) -> 'SimpleGlyphTable':
        num_contours = stream.read_int16()
        x_min = stream.read_int16()
        y_min = stream.read_int16()
        x_max = stream.read_int16()
        y_max = stream.read_int16()
        end_pts_of_contours = [stream.read_uint16() for _ in range(num_contours)]
        num_coordinates = end_pts_of_contours[-1] + 1
        instruction_length = stream.read_uint16()
        instructions = stream.read(instruction_length)

        flags_list = []
        while len(flags_list) < num_coordinates:
            flags = SimpleGlyphFlags.parse(stream.read_uint8())
            if flags.repeat_flag:
                repeat_times = stream.read_uint8() + 1
            else:
                repeat_times = 1
            for _ in range(repeat_times):
                flags_list.append(flags)
        if len(flags_list) != num_coordinates:
            raise SfntError('[glyf] bad number of coordinates')

        x_coordinates = []
        for flags in flags_list:
            if flags.x_short_vector:
                x = stream.read_uint8()
                if not flags.x_is_same_or_positive_x_short_vector:
                    x *= -1
            elif flags.x_is_same_or_positive_x_short_vector:
                x = 0
            else:
                x = stream.read_int16()
            x_coordinates.append(x)

        y_coordinates = []
        for flags in flags_list:
            if flags.y_short_vector:
                y = stream.read_uint8()
                if not flags.y_is_same_or_positive_y_short_vector:
                    y *= -1
            elif flags.y_is_same_or_positive_y_short_vector:
                y = 0
            else:
                y = stream.read_int16()
            y_coordinates.append(y)

        coordinates = []
        for flags, (x, y) in zip(flags_list, zip(x_coordinates, y_coordinates)):
            coordinates.append(GlyphCoordinate(flags, x, y))

        return SimpleGlyphTable(
            x_min,
            y_min,
            x_max,
            y_max,
            end_pts_of_contours,
            instructions,
            coordinates,
            flags_list[0].overlap_simple,
        )

    x_min: int
    y_min: int
    x_max: int
    y_max: int
    end_pts_of_contours: list[int]
    instructions: bytes
    coordinates: list[GlyphCoordinate]
    overlap_simple: bool

    def __init__(
            self,
            x_min: int = 0,
            y_min: int = 0,
            x_max: int = 0,
            y_max: int = 0,
            end_pts_of_contours: list[int] | None = None,
            instructions: bytes = b'',
            coordinates: list[GlyphCoordinate] | None = None,
            overlap_simple: bool = False,
    ):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.end_pts_of_contours = [] if end_pts_of_contours is None else end_pts_of_contours
        self.instructions = instructions
        self.coordinates = [] if coordinates is None else coordinates
        self.overlap_simple = overlap_simple

    @property
    def num_contours(self) -> int:
        return len(self.end_pts_of_contours)

    def copy(self) -> 'SimpleGlyphTable':
        return SimpleGlyphTable(
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
            self.end_pts_of_contours,
            self.instructions,
            self.coordinates,
            self.overlap_simple,
        )

    def dump(self) -> bytes:

        # TODO

        pass
