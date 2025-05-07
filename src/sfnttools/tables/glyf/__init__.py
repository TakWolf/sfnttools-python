from io import BytesIO

from sfnttools.error import SfntError
from sfnttools.table import SfntTableReader, SfntTableWriter, SfntTable
from sfnttools.tables.glyf.component import ComponentGlyph
from sfnttools.tables.glyf.simple import SimpleGlyph
from sfnttools.tables.loca import LocaTable
from sfnttools.utils.stream import Stream


class GlyfTable(SfntTable):
    @staticmethod
    def parse(data: bytes, reader: SfntTableReader) -> 'GlyfTable':
        loca_table: LocaTable = reader.get_or_parse_table('loca')

        glyph_descriptions = []
        for i in range(len(loca_table.offsets) - 1):
            offset = loca_table.offsets[i]
            next_offset = loca_table.offsets[i + 1]
            glyph_data = data[offset:next_offset]
            if glyph_data == b'':
                glyph_description = None
            else:
                num_contours = int.from_bytes(glyph_data[0:2], 'big', signed=True)
                if num_contours > 0:
                    glyph_description = SimpleGlyph.parse(glyph_data)
                elif num_contours < 0:
                    glyph_description = ComponentGlyph.parse(glyph_data)
                else:
                    raise SfntError('[glyf] bad glyph data')
            glyph_descriptions.append(glyph_description)

        return GlyfTable(glyph_descriptions)

    glyph_descriptions: list[SimpleGlyph | ComponentGlyph | None]

    def __init__(
            self,
            glyph_descriptions: list[SimpleGlyph | ComponentGlyph | None] | None = None,
    ):
        self.glyph_descriptions = [] if glyph_descriptions is None else glyph_descriptions

    def copy(self) -> 'GlyfTable':
        glyph_descriptions = []
        for glyph_description in self.glyph_descriptions:
            glyph_descriptions.append(None if glyph_description is None else glyph_description.copy())
        return GlyfTable(glyph_descriptions)

    def dump(self, writer: SfntTableWriter) -> bytes:
        buffer = BytesIO()
        stream = Stream(buffer)

        # TODO

        return buffer.getvalue()
