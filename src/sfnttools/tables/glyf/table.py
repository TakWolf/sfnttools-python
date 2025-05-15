from typing import Any

from sfnttools.configs import GlyfDataOffsetsPaddingMode, SfntConfigs
from sfnttools.error import SfntError
from sfnttools.table import SfntTable
from sfnttools.tables.glyf.component import ComponentGlyph
from sfnttools.tables.glyf.simple import SimpleGlyph
from sfnttools.tables.loca.table import LocaTable
from sfnttools.utils.stream import Stream


class GlyfTable(SfntTable):
    parse_dependencies = ['loca']

    @staticmethod
    def parse(data: bytes, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> 'GlyfTable':
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
                    glyph = SimpleGlyph.parse_body(stream, num_contours, x_min, y_min, x_max, y_max)
                elif num_contours < 0:
                    glyph = ComponentGlyph.parse_body(stream, x_min, y_min, x_max, y_max)
                else:
                    raise SfntError('[glyf] bad glyph data')
            glyphs.append(glyph)

        return GlyfTable(glyphs)

    glyphs: list[SimpleGlyph | ComponentGlyph | None]

    def __init__(self, glyphs: list[SimpleGlyph | ComponentGlyph | None] | None = None):
        self.glyphs = [] if glyphs is None else glyphs

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GlyfTable):
            return False
        return self.glyphs == other.glyphs

    @property
    def num_glyphs(self) -> int:
        return len(self.glyphs)

    def copy(self) -> 'GlyfTable':
        glyphs = []
        for glyph in self.glyphs:
            glyphs.append(None if glyph is None else glyph.copy())
        return GlyfTable(glyphs)

    def dump(self, configs: SfntConfigs, dependencies: dict[str, SfntTable]) -> tuple[bytes, dict[str, SfntTable]]:
        stream = Stream()

        offsets = []
        for glyph in self.glyphs:
            offsets.append(stream.tell())
            if glyph is not None:
                stream.write(glyph.dump())
            if configs.glyf_data_offsets_padding_mode == GlyfDataOffsetsPaddingMode.ALIGN_TO_2_BYTE:
                stream.align_to_2_byte_with_nulls()
            elif configs.glyf_data_offsets_padding_mode == GlyfDataOffsetsPaddingMode.ALIGN_TO_4_BYTE:
                stream.align_to_4_byte_with_nulls()
        offsets.append(stream.tell())

        return stream.get_value(), {'loca': LocaTable(offsets)}
