from io import BytesIO

from sfnttools.error import SfntError
from sfnttools.table import SfntTable
from sfnttools.tables.glyf.component import XyGlyphComponent, PointsGlyphComponent, ComponentGlyph
from sfnttools.tables.glyf.simple import GlyphCoordinate, SimpleGlyph
from sfnttools.tables.loca import LocaTable
from sfnttools.utils.stream import Stream


class GlyfTable(SfntTable):
    parse_dependencies = ['loca']

    @staticmethod
    def parse(data: bytes, dependencies: dict[str, SfntTable]) -> 'GlyfTable':
        loca_table: LocaTable = dependencies['loca']

        glyphs = []
        for i in range(len(loca_table.offsets) - 1):
            offset = loca_table.offsets[i]
            next_offset = loca_table.offsets[i + 1]
            glyph_data = data[offset:next_offset]
            if glyph_data == b'':
                glyph = None
            else:
                stream = Stream(glyph_data)

                num_contours = stream.read_int16()
                x_min = stream.read_int16()
                y_min = stream.read_int16()
                x_max = stream.read_int16()
                y_max = stream.read_int16()

                if num_contours > 0:
                    glyph = SimpleGlyph.parse(stream, num_contours, x_min, y_min, x_max, y_max)
                elif num_contours < 0:
                    glyph = ComponentGlyph.parse(stream, x_min, y_min, x_max, y_max)
                else:
                    raise SfntError('[glyf] bad glyph data')
            glyphs.append(glyph)

        return GlyfTable(glyphs)

    glyphs: list[SimpleGlyph | ComponentGlyph | None]

    def __init__(self, glyphs: list[SimpleGlyph | ComponentGlyph | None] | None = None):
        self.glyphs = [] if glyphs is None else glyphs

    def copy(self) -> 'GlyfTable':
        glyphs = []
        for glyph in self.glyphs:
            glyphs.append(None if glyph is None else glyph.copy())
        return GlyfTable(glyphs)

    def dump(self, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        buffer = BytesIO()
        stream = Stream(buffer)

        # TODO

        return buffer.getvalue(), {'loca': LocaTable()}
