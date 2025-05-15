import math

from sfnttools.error import SfntError
from sfnttools.flags import SfntFlags
from sfnttools.tables.glyf.component import ComponentGlyph
from sfnttools.tables.glyf.simple import GlyphCoordinate, SimpleGlyph
from sfnttools.tables.glyf.table import GlyfTable
from sfnttools.tables.head.enum import IndexToLocFormat
from sfnttools.utils.stream import Stream

_OPTION_FLAGS_MASK_HAS_OVERLAP_SIMPLE_BITMAP = 0b_0000_0000_0000_0001

_TRANSFORMED_GLYF_FLAGS_MASK_ON_CURVE_POINT = 0b_1000_0000
_TRANSFORMED_GLYF_FLAGS_MASK_OTHERS = 0b_0111_1111


class OptionFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'OptionFlags':
        has_overlap_simple_bitmap = value & _OPTION_FLAGS_MASK_HAS_OVERLAP_SIMPLE_BITMAP > 0
        return OptionFlags(has_overlap_simple_bitmap)

    has_overlap_simple_bitmap: bool

    def __init__(self, has_overlap_simple_bitmap: bool = False):
        self.has_overlap_simple_bitmap = has_overlap_simple_bitmap

    @property
    def value(self) -> int:
        value = 0
        if self.has_overlap_simple_bitmap:
            value |= _OPTION_FLAGS_MASK_HAS_OVERLAP_SIMPLE_BITMAP
        return value

    def copy(self) -> 'SfntFlags':
        return OptionFlags(self.has_overlap_simple_bitmap)


class TransformedGlyfTable:
    @staticmethod
    def parse(data: bytes) -> 'TransformedGlyfTable':
        stream = Stream(data)

        stream.read_uint16()
        option_flags = OptionFlags.parse(stream.read_uint16())
        num_glyphs = stream.read_uint16()
        index_format = IndexToLocFormat(stream.read_uint16())

        n_contour_stream_size = stream.read_uint32()
        n_points_stream_size = stream.read_uint32()
        flag_stream_size = stream.read_uint32()
        glyph_stream_size = stream.read_uint32()
        composite_stream_size = stream.read_uint32()
        bbox_bitmap_size = math.ceil(num_glyphs / 32) * 4
        bbox_stream_size = stream.read_uint32() - bbox_bitmap_size
        instruction_stream_size = stream.read_uint32()

        n_contour_stream = stream.read(n_contour_stream_size)
        n_points_stream = stream.read(n_points_stream_size)
        flag_stream = stream.read(flag_stream_size)
        glyph_stream = stream.read(glyph_stream_size)
        composite_stream = stream.read(composite_stream_size)
        bbox_bitmap = stream.read_binary_string(bbox_bitmap_size)
        bbox_stream = stream.read(bbox_stream_size)
        instruction_stream = stream.read(instruction_stream_size)
        if option_flags.has_overlap_simple_bitmap:
            overlap_simple_bitmap_size = math.ceil(num_glyphs / 8)
            overlap_simple_bitmap = stream.read_binary_string(overlap_simple_bitmap_size)
        else:
            overlap_simple_bitmap = None

        return TransformedGlyfTable(
            num_glyphs,
            index_format,
            n_contour_stream,
            n_points_stream,
            flag_stream,
            glyph_stream,
            composite_stream,
            bbox_bitmap,
            bbox_stream,
            instruction_stream,
            overlap_simple_bitmap,
        )

    @staticmethod
    def transform(glyf_table: GlyfTable, index_format: IndexToLocFormat) -> 'TransformedGlyfTable':
        n_contour_stream = Stream()
        n_points_stream = Stream()
        flag_stream = Stream()
        glyph_stream = Stream()
        composite_stream = Stream()
        bbox_bitmap = []
        bbox_stream = Stream()
        instruction_stream = Stream()
        overlap_simple_bitmap = []

        for glyph in glyf_table.glyphs:
            if isinstance(glyph, SimpleGlyph):
                n_contour_stream.write_int16(glyph.num_contours)

                n_point = 0
                for end_point in glyph.end_pts_of_contours:
                    end_point += 1
                    n_points_stream.write_255uint16(end_point - n_point)
                    n_point = end_point

                for coordinate in glyph.coordinates:
                    abs_delta_x = abs(coordinate.delta_x)
                    abs_delta_y = abs(coordinate.delta_y)

                    if coordinate.delta_x == 0 and abs_delta_y <= 1279:
                        glyph_stream.write_uint8(abs_delta_y % 256)
                        flags = abs_delta_y // 256 * 2
                        if coordinate.delta_y >= 0:
                            flags += 1
                    elif coordinate.delta_y == 0 and abs_delta_x <= 1279:
                        glyph_stream.write_uint8(abs_delta_x % 256)
                        flags = abs_delta_x // 256 * 2
                        if coordinate.delta_x >= 0:
                            flags += 1
                        flags += 10
                    elif 1 <= abs_delta_x <= 64 and 1 <= abs_delta_y <= 64:
                        glyph_stream.write_uint8(((abs_delta_x - 1) % 16) << 4 | (abs_delta_y - 1) % 16)
                        flags = (abs_delta_x - 1) // 16 * 16 + (abs_delta_y - 1) // 16 * 4
                        if coordinate.delta_y >= 0:
                            flags += 2
                        if coordinate.delta_x >= 0:
                            flags += 1
                        flags += 20
                    elif 1 <= abs_delta_x <= 768 and 1 <= abs_delta_y <= 768:
                        glyph_stream.write_uint8((abs_delta_x - 1) % 256)
                        glyph_stream.write_uint8((abs_delta_y - 1) % 256)
                        flags = (abs_delta_x - 1) // 256 * 12 + (abs_delta_y - 1) // 256 * 4
                        if coordinate.delta_y >= 0:
                            flags += 2
                        if coordinate.delta_x >= 0:
                            flags += 1
                        flags += 84
                    elif abs_delta_x <= 0xFFFFFFFFFFFF and abs_delta_y <= 0xFFFFFFFFFFFF:
                        glyph_stream.write_uint24(abs_delta_x << 12 | abs_delta_y)
                        flags = 0
                        if coordinate.delta_y >= 0:
                            flags += 2
                        if coordinate.delta_x >= 0:
                            flags += 1
                        flags += 120
                    else:
                        glyph_stream.write_uint16(abs_delta_x)
                        glyph_stream.write_uint16(abs_delta_y)
                        flags = 0
                        if coordinate.delta_y >= 0:
                            flags += 2
                        if coordinate.delta_x >= 0:
                            flags += 1
                        flags += 124

                    if not coordinate.on_curve_point:
                        flags |= _TRANSFORMED_GLYF_FLAGS_MASK_ON_CURVE_POINT

                    flag_stream.write_uint8(flags)

                glyph_stream.write_255uint16(len(glyph.instructions))
                instruction_stream.write(glyph.instructions)

                bbox_bitmap.append('0')
                overlap_simple_bitmap.append('1' if glyph.overlap_simple else '0')
            elif isinstance(glyph, ComponentGlyph):
                n_contour_stream.write_int16(-1)

                bbox_stream.write_int16(glyph.x_min)
                bbox_stream.write_int16(glyph.y_min)
                bbox_stream.write_int16(glyph.x_max)
                bbox_stream.write_int16(glyph.y_max)

                glyph.dump_body(composite_stream)

                bbox_bitmap.append('1')
                overlap_simple_bitmap.append('0')
            else:
                n_contour_stream.write_int16(0)

                bbox_bitmap.append('0')
                overlap_simple_bitmap.append('0')

        num_glyphs = len(glyf_table.glyphs)

        bbox_bitmap_length = math.ceil(num_glyphs / 32) * 4 * 8
        while len(bbox_bitmap) < bbox_bitmap_length:
            bbox_bitmap.append('0')
        bbox_bitmap = ''.join(bbox_bitmap)

        if '1' in overlap_simple_bitmap:
            overlap_simple_bitmap_length = math.ceil(num_glyphs / 8) * 8
            while len(overlap_simple_bitmap) < overlap_simple_bitmap_length:
                overlap_simple_bitmap.append('0')
            overlap_simple_bitmap = ''.join(overlap_simple_bitmap)
        else:
            overlap_simple_bitmap = None

        return TransformedGlyfTable(
            num_glyphs,
            index_format,
            n_contour_stream.get_value(),
            n_points_stream.get_value(),
            flag_stream.get_value(),
            glyph_stream.get_value(),
            composite_stream.get_value(),
            bbox_bitmap,
            bbox_stream.get_value(),
            instruction_stream.get_value(),
            overlap_simple_bitmap,
        )

    num_glyphs: int
    index_format: IndexToLocFormat
    n_contour_stream: bytes
    n_points_stream: bytes
    flag_stream: bytes
    glyph_stream: bytes
    composite_stream: bytes
    bbox_bitmap: str
    bbox_stream: bytes
    instruction_stream: bytes
    overlap_simple_bitmap: str | None

    def __init__(
            self,
            num_glyphs: int,
            index_format: IndexToLocFormat,
            n_contour_stream: bytes,
            n_points_stream: bytes,
            flag_stream: bytes,
            glyph_stream: bytes,
            composite_stream: bytes,
            bbox_bitmap: str,
            bbox_stream: bytes,
            instruction_stream: bytes,
            overlap_simple_bitmap: str | None,
    ):
        self.num_glyphs = num_glyphs
        self.index_format = index_format
        self.n_contour_stream = n_contour_stream
        self.n_points_stream = n_points_stream
        self.flag_stream = flag_stream
        self.glyph_stream = glyph_stream
        self.composite_stream = composite_stream
        self.bbox_bitmap = bbox_bitmap
        self.bbox_stream = bbox_stream
        self.instruction_stream = instruction_stream
        self.overlap_simple_bitmap = overlap_simple_bitmap

    def reconstruct(self) -> GlyfTable:
        n_contour_stream = Stream(self.n_contour_stream)
        n_points_stream = Stream(self.n_points_stream)
        flag_stream = Stream(self.flag_stream)
        glyph_stream = Stream(self.glyph_stream)
        composite_stream = Stream(self.composite_stream)
        bbox_stream = Stream(self.bbox_stream)
        instruction_stream = Stream(self.instruction_stream)

        glyphs = []
        for i in range(self.num_glyphs):
            num_contours = n_contour_stream.read_int16()
            if num_contours > 0:
                end_pts_of_contours = []
                n_points = 0
                for _ in range(num_contours):
                    n_points += n_points_stream.read_255uint16()
                    end_pts_of_contours.append(n_points - 1)

                coordinates = []
                for _ in range(n_points):
                    flags = flag_stream.read_uint8()
                    on_curve_point = flags & _TRANSFORMED_GLYF_FLAGS_MASK_ON_CURVE_POINT == 0
                    flags = flags & _TRANSFORMED_GLYF_FLAGS_MASK_OTHERS

                    if flags < 10:
                        delta_x = 0
                        delta_y = glyph_stream.read_uint8()
                        delta_y += flags // 2 * 256
                        if flags % 2 == 0:
                            delta_y *= -1
                    elif flags < 20:
                        flags -= 10
                        delta_y = 0
                        delta_x = glyph_stream.read_uint8()
                        delta_x += flags // 2 * 256
                        if flags % 2 == 0:
                            delta_x *= -1
                    elif flags < 84:
                        flags -= 20
                        delta_xy = glyph_stream.read_uint8()
                        delta_x = delta_xy >> 4
                        delta_y = delta_xy & 0b_0000_1111
                        delta_x += flags // 16 * 16 + 1
                        delta_y += flags % 16 // 4 * 16 + 1
                        if flags % 2 == 0:
                            delta_x *= -1
                        if flags // 2 % 2 == 0:
                            delta_y *= -1
                    elif flags < 120:
                        flags -= 84
                        delta_x = glyph_stream.read_uint8()
                        delta_y = glyph_stream.read_uint8()
                        delta_x += flags // 12 * 256 + 1
                        delta_y += flags % 12 // 4 * 256 + 1
                        if flags % 2 == 0:
                            delta_x *= -1
                        if flags // 2 % 2 == 0:
                            delta_y *= -1
                    elif flags < 124:
                        flags -= 120
                        delta_xy = glyph_stream.read_uint24()
                        delta_x = delta_xy >> 12
                        delta_y = delta_xy & 0b_0000_0000_0000_1111_1111_1111
                        if flags % 2 == 0:
                            delta_x *= -1
                        if flags // 2 % 2 == 0:
                            delta_y *= -1
                    else:
                        flags -= 124
                        delta_x = glyph_stream.read_uint16()
                        delta_y = glyph_stream.read_uint16()
                        if flags % 2 == 0:
                            delta_x *= -1
                        if flags // 2 % 2 == 0:
                            delta_y *= -1

                    coordinates.append(GlyphCoordinate(on_curve_point, delta_x, delta_y))

                instruction_length = glyph_stream.read_255uint16()
                instructions = instruction_stream.read(instruction_length)

                if self.overlap_simple_bitmap is None:
                    overlap_simple = False
                else:
                    overlap_simple = self.overlap_simple_bitmap[i] == '1'

                if self.bbox_bitmap[i] == '1':
                    x_min = bbox_stream.read_int16()
                    y_min = bbox_stream.read_int16()
                    x_max = bbox_stream.read_int16()
                    y_max = bbox_stream.read_int16()
                else:
                    x_min, y_min, x_max, y_max = GlyphCoordinate.calculate_bounds(coordinates)

                glyph = SimpleGlyph(
                    x_min,
                    y_min,
                    x_max,
                    y_max,
                    end_pts_of_contours,
                    coordinates,
                    instructions,
                    overlap_simple,
                )
            elif num_contours < 0:
                if self.bbox_bitmap[i] != '1':
                    raise SfntError("woff2 transformed component glyph must set bounds")

                x_min = bbox_stream.read_int16()
                y_min = bbox_stream.read_int16()
                x_max = bbox_stream.read_int16()
                y_max = bbox_stream.read_int16()

                glyph = ComponentGlyph.parse_body(composite_stream, x_min, y_min, x_max, y_max)
            else:
                glyph = None
            glyphs.append(glyph)

        return GlyfTable(glyphs)

    def dump(self) -> bytes:
        option_flags = OptionFlags(
            has_overlap_simple_bitmap=self.overlap_simple_bitmap is not None,
        )

        stream = Stream()

        stream.write_uint16(0)
        stream.write_uint16(option_flags.value)
        stream.write_uint16(self.num_glyphs)
        stream.write_uint16(self.index_format)

        stream.write_uint32(len(self.n_contour_stream))
        stream.write_uint32(len(self.n_points_stream))
        stream.write_uint32(len(self.flag_stream))
        stream.write_uint32(len(self.glyph_stream))
        stream.write_uint32(len(self.composite_stream))
        stream.write_uint32(len(self.bbox_bitmap) // 8 + len(self.bbox_stream))
        stream.write_uint32(len(self.instruction_stream))

        stream.write(self.n_contour_stream)
        stream.write(self.n_points_stream)
        stream.write(self.flag_stream)
        stream.write(self.glyph_stream)
        stream.write(self.composite_stream)
        stream.write_binary_string(self.bbox_bitmap)
        stream.write(self.bbox_stream)
        stream.write(self.instruction_stream)
        if self.overlap_simple_bitmap is not None:
            stream.write_binary_string(self.overlap_simple_bitmap)

        return stream.get_value()
