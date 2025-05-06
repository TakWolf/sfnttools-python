from io import BytesIO

from sfnttools.table import SfntTableContainer, SfntTable
from sfnttools.tables.glyf.composite import ComponentGlyphRecord
from sfnttools.tables.glyf.description import GlyphDescription
from sfnttools.tables.glyf.simple import SimpleGlyphTable
from sfnttools.tables.loca import LocaTable
from sfnttools.utils.stream import Stream


class GlyfTable(SfntTable):
    @staticmethod
    def parse(data: bytes, container: SfntTableContainer) -> 'GlyfTable':
        loca_table: LocaTable = container.get_table('loca')

        glyph_descriptions = []
        for i in range(len(loca_table.offsets) - 1):
            offset = loca_table.offsets[i]
            next_offset = loca_table.offsets[i + 1]
            glyph_data = data[offset:next_offset]
            if glyph_data == b'':
                glyph_description = None
            else:
                stream = Stream(glyph_data)
                num_contours = stream.read_int16()
                stream.seek(0)
                if num_contours >= 0:
                    glyph_description = SimpleGlyphTable.parse(stream)
                else:
                    glyph_description = ComponentGlyphRecord.parse(stream)
            glyph_descriptions.append(glyph_description)

        return GlyfTable(glyph_descriptions)

    glyph_descriptions: list[GlyphDescription | None]

    def __init__(self,  glyph_descriptions: list[GlyphDescription | None] | None = None):
        self.glyph_descriptions = [] if glyph_descriptions is None else glyph_descriptions

    def copy(self) -> 'GlyfTable':
        glyph_descriptions = []
        for glyph_description in self.glyph_descriptions:
            if glyph_description is None:
                glyph_descriptions.append(None)
            else:
                glyph_descriptions.append(glyph_description.copy())
        return GlyfTable(glyph_descriptions)

    def dump(self, container: SfntTableContainer) -> bytes:
        buffer = BytesIO()
        stream = Stream(buffer)

        # TODO

        return buffer.getvalue()
