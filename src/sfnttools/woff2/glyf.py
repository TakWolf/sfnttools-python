import math
from io import BytesIO

from sfnttools.flags import SfntFlags
from sfnttools.tables.head import IndexToLocFormat
from sfnttools.utils.stream import Stream

_OPTION_FLAGS_MASK_HAS_OVERLAP_SIMPLE_BITMAP = 0b_0000_0000_0000_0001


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
        bbox_bitmap = stream.read(bbox_bitmap_size)
        bbox_stream = stream.read(bbox_stream_size)
        instruction_stream = stream.read(instruction_stream_size)
        if option_flags.has_overlap_simple_bitmap:
            overlap_simple_bitmap_size = math.ceil(num_glyphs / 8)
            overlap_simple_bitmap = stream.read(overlap_simple_bitmap_size)
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

    num_glyphs: int
    index_format: IndexToLocFormat
    n_contour_stream: bytes
    n_points_stream: bytes
    flag_stream: bytes
    glyph_stream: bytes
    composite_stream: bytes
    bbox_bitmap: bytes
    bbox_stream: bytes
    instruction_stream: bytes
    overlap_simple_bitmap: bytes | None

    def __init__(
            self,
            num_glyphs: int,
            index_format: IndexToLocFormat,
            n_contour_stream: bytes,
            n_points_stream: bytes,
            flag_stream: bytes,
            glyph_stream: bytes,
            composite_stream: bytes,
            bbox_bitmap: bytes,
            bbox_stream: bytes,
            instruction_stream: bytes,
            overlap_simple_bitmap: bytes | None,
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

    def dump(self) -> bytes:
        option_flags = OptionFlags(
            has_overlap_simple_bitmap=self.overlap_simple_bitmap is not None,
        )

        buffer = BytesIO()
        stream = Stream(buffer)

        stream.write_uint16(0)
        stream.write_uint16(option_flags.value)
        stream.write_uint16(self.num_glyphs)
        stream.write_uint16(self.index_format)

        stream.write_uint32(len(self.n_contour_stream))
        stream.write_uint32(len(self.n_points_stream))
        stream.write_uint32(len(self.flag_stream))
        stream.write_uint32(len(self.glyph_stream))
        stream.write_uint32(len(self.composite_stream))
        stream.write_uint32(len(self.bbox_bitmap) + len(self.bbox_stream))
        stream.write_uint32(len(self.instruction_stream))

        stream.write(self.n_contour_stream)
        stream.write(self.n_points_stream)
        stream.write(self.flag_stream)
        stream.write(self.glyph_stream)
        stream.write(self.composite_stream)
        stream.write(self.bbox_bitmap)
        stream.write(self.bbox_stream)
        stream.write(self.instruction_stream)
        if self.overlap_simple_bitmap is not None:
            stream.write(self.overlap_simple_bitmap)

        return buffer.getvalue()
