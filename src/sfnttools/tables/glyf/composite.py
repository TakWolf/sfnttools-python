from typing import Final

from sfnttools.table import SfntFlags
from sfnttools.tables.glyf.description import GlyphDescription
from sfnttools.utils.stream import Stream

COMPONENT_GLYPH_FLAGS_MASK_ARG_1_AND_2_ARE_WORDS: Final = 0b_0000_0000_0000_0001
COMPONENT_GLYPH_FLAGS_MASK_ARGS_ARE_XY_VALUES: Final = 0b_0000_0000_0000_0010
COMPONENT_GLYPH_FLAGS_MASK_ROUND_XY_TO_GRID: Final = 0b_0000_0000_0000_0100
COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_SCALE: Final = 0b_0000_0000_0000_1000
COMPONENT_GLYPH_FLAGS_MASK_MORE_COMPONENTS: Final = 0b_0000_0000_0010_0000
COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_AN_X_AND_Y_SCALE: Final = 0b_0000_0000_0100_0000
COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_TWO_BY_TWO: Final = 0b_0000_0000_1000_0000
COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_INSTRUCTIONS: Final = 0b_0000_0001_0000_0000
COMPONENT_GLYPH_FLAGS_MASK_USE_MY_METRICS: Final = 0b_0000_0010_0000_0000
COMPONENT_GLYPH_FLAGS_MASK_OVERLAP_COMPOUND: Final = 0b_0000_0100_0000_0000
COMPONENT_GLYPH_FLAGS_MASK_SCALED_COMPONENT_OFFSET: Final = 0b_0000_1000_0000_0000
COMPONENT_GLYPH_FLAGS_MASK_UNSCALED_COMPONENT_OFFSET: Final = 0b_0001_0000_0000_0000


class ComponentGlyphFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'ComponentGlyphFlags':
        arg_1_and_2_are_words = value & COMPONENT_GLYPH_FLAGS_MASK_ARG_1_AND_2_ARE_WORDS > 0
        args_are_xy_values = value & COMPONENT_GLYPH_FLAGS_MASK_ARGS_ARE_XY_VALUES > 0
        round_xy_to_grid = value & COMPONENT_GLYPH_FLAGS_MASK_ROUND_XY_TO_GRID > 0
        we_have_a_scale = value & COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_SCALE > 0
        more_components = value & COMPONENT_GLYPH_FLAGS_MASK_MORE_COMPONENTS > 0
        we_have_an_x_and_y_scale = value & COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_AN_X_AND_Y_SCALE > 0
        we_have_a_two_by_two = value & COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_TWO_BY_TWO > 0
        we_have_instructions = value & COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_INSTRUCTIONS > 0
        use_my_metrics = value & COMPONENT_GLYPH_FLAGS_MASK_USE_MY_METRICS > 0
        overlap_compound = value & COMPONENT_GLYPH_FLAGS_MASK_OVERLAP_COMPOUND > 0
        scaled_component_offset = value & COMPONENT_GLYPH_FLAGS_MASK_SCALED_COMPONENT_OFFSET > 0
        unscaled_component_offset = value & COMPONENT_GLYPH_FLAGS_MASK_UNSCALED_COMPONENT_OFFSET > 0
        return ComponentGlyphFlags(
            arg_1_and_2_are_words,
            args_are_xy_values,
            round_xy_to_grid,
            we_have_a_scale,
            more_components,
            we_have_an_x_and_y_scale,
            we_have_a_two_by_two,
            we_have_instructions,
            use_my_metrics,
            overlap_compound,
            scaled_component_offset,
            unscaled_component_offset,
        )

    arg_1_and_2_are_words: bool
    args_are_xy_values: bool
    round_xy_to_grid: bool
    we_have_a_scale: bool
    more_components: bool
    we_have_an_x_and_y_scale: bool
    we_have_a_two_by_two: bool
    we_have_instructions: bool
    use_my_metrics: bool
    overlap_compound: bool
    scaled_component_offset: bool
    unscaled_component_offset: bool

    def __init__(
            self,
            arg_1_and_2_are_words: bool = False,
            args_are_xy_values: bool = False,
            round_xy_to_grid: bool = False,
            we_have_a_scale: bool = False,
            more_components: bool = False,
            we_have_an_x_and_y_scale: bool = False,
            we_have_a_two_by_two: bool = False,
            we_have_instructions: bool = False,
            use_my_metrics: bool = False,
            overlap_compound: bool = False,
            scaled_component_offset: bool = False,
            unscaled_component_offset: bool = False,
    ):
        self.arg_1_and_2_are_words = arg_1_and_2_are_words
        self.args_are_xy_values = args_are_xy_values
        self.round_xy_to_grid = round_xy_to_grid
        self.we_have_a_scale = we_have_a_scale
        self.more_components = more_components
        self.we_have_an_x_and_y_scale = we_have_an_x_and_y_scale
        self.we_have_a_two_by_two = we_have_a_two_by_two
        self.we_have_instructions = we_have_instructions
        self.use_my_metrics = use_my_metrics
        self.overlap_compound = overlap_compound
        self.scaled_component_offset = scaled_component_offset
        self.unscaled_component_offset = unscaled_component_offset

    @property
    def value(self) -> int:
        value = 0
        if self.arg_1_and_2_are_words:
            value |= COMPONENT_GLYPH_FLAGS_MASK_ARG_1_AND_2_ARE_WORDS
        if self.args_are_xy_values:
            value |= COMPONENT_GLYPH_FLAGS_MASK_ARGS_ARE_XY_VALUES
        if self.round_xy_to_grid:
            value |= COMPONENT_GLYPH_FLAGS_MASK_ROUND_XY_TO_GRID
        if self.we_have_a_scale:
            value |= COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_SCALE
        if self.more_components:
            value |= COMPONENT_GLYPH_FLAGS_MASK_MORE_COMPONENTS
        if self.we_have_an_x_and_y_scale:
            value |= COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_AN_X_AND_Y_SCALE
        if self.we_have_a_two_by_two:
            value |= COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_TWO_BY_TWO
        if self.we_have_instructions:
            value |= COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_INSTRUCTIONS
        if self.use_my_metrics:
            value |= COMPONENT_GLYPH_FLAGS_MASK_USE_MY_METRICS
        if self.overlap_compound:
            value |= COMPONENT_GLYPH_FLAGS_MASK_OVERLAP_COMPOUND
        if self.scaled_component_offset:
            value |= COMPONENT_GLYPH_FLAGS_MASK_SCALED_COMPONENT_OFFSET
        if self.unscaled_component_offset:
            value |= COMPONENT_GLYPH_FLAGS_MASK_UNSCALED_COMPONENT_OFFSET
        return value

    def copy(self) -> 'ComponentGlyphFlags':
        return ComponentGlyphFlags(
            self.arg_1_and_2_are_words,
            self.args_are_xy_values,
            self.round_xy_to_grid,
            self.we_have_a_scale,
            self.more_components,
            self.we_have_an_x_and_y_scale,
            self.we_have_a_two_by_two,
            self.we_have_instructions,
            self.use_my_metrics,
            self.overlap_compound,
            self.scaled_component_offset,
            self.unscaled_component_offset,
        )


class ComponentGlyphRecord(GlyphDescription):
    @staticmethod
    def parse(stream: Stream) -> 'ComponentGlyphRecord':
        pass

    def copy(self) -> 'ComponentGlyphRecord':
        pass

    def dump(self) -> bytes:
        pass
