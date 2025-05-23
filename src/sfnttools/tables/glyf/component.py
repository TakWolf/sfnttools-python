from __future__ import annotations

from typing import Any

from sfnttools.error import SfntError
from sfnttools.flags import SfntFlags
from sfnttools.utils.stream import Stream

_COMPONENT_GLYPH_FLAGS_MASK_ARG_1_AND_2_ARE_WORDS = 0b_0000_0000_0000_0001
_COMPONENT_GLYPH_FLAGS_MASK_ARGS_ARE_XY_VALUES = 0b_0000_0000_0000_0010
_COMPONENT_GLYPH_FLAGS_MASK_ROUND_XY_TO_GRID = 0b_0000_0000_0000_0100
_COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_SCALE = 0b_0000_0000_0000_1000
_COMPONENT_GLYPH_FLAGS_MASK_MORE_COMPONENTS = 0b_0000_0000_0010_0000
_COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_AN_X_AND_Y_SCALE = 0b_0000_0000_0100_0000
_COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_TWO_BY_TWO = 0b_0000_0000_1000_0000
_COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_INSTRUCTIONS = 0b_0000_0001_0000_0000
_COMPONENT_GLYPH_FLAGS_MASK_USE_MY_METRICS = 0b_0000_0010_0000_0000
_COMPONENT_GLYPH_FLAGS_MASK_OVERLAP_COMPOUND = 0b_0000_0100_0000_0000
_COMPONENT_GLYPH_FLAGS_MASK_SCALED_COMPONENT_OFFSET = 0b_0000_1000_0000_0000
_COMPONENT_GLYPH_FLAGS_MASK_UNSCALED_COMPONENT_OFFSET = 0b_0001_0000_0000_0000


class ComponentGlyphFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> ComponentGlyphFlags:
        arg_1_and_2_are_words = value & _COMPONENT_GLYPH_FLAGS_MASK_ARG_1_AND_2_ARE_WORDS > 0
        args_are_xy_values = value & _COMPONENT_GLYPH_FLAGS_MASK_ARGS_ARE_XY_VALUES > 0
        round_xy_to_grid = value & _COMPONENT_GLYPH_FLAGS_MASK_ROUND_XY_TO_GRID > 0
        we_have_a_scale = value & _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_SCALE > 0
        more_components = value & _COMPONENT_GLYPH_FLAGS_MASK_MORE_COMPONENTS > 0
        we_have_an_x_and_y_scale = value & _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_AN_X_AND_Y_SCALE > 0
        we_have_a_two_by_two = value & _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_TWO_BY_TWO > 0
        we_have_instructions = value & _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_INSTRUCTIONS > 0
        use_my_metrics = value & _COMPONENT_GLYPH_FLAGS_MASK_USE_MY_METRICS > 0
        overlap_compound = value & _COMPONENT_GLYPH_FLAGS_MASK_OVERLAP_COMPOUND > 0
        scaled_component_offset = value & _COMPONENT_GLYPH_FLAGS_MASK_SCALED_COMPONENT_OFFSET > 0
        unscaled_component_offset = value & _COMPONENT_GLYPH_FLAGS_MASK_UNSCALED_COMPONENT_OFFSET > 0
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

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ComponentGlyphFlags):
            return False
        return (self.arg_1_and_2_are_words == other.arg_1_and_2_are_words and
                self.args_are_xy_values == other.args_are_xy_values and
                self.round_xy_to_grid == other.round_xy_to_grid and
                self.we_have_a_scale == other.we_have_a_scale and
                self.more_components == other.more_components and
                self.we_have_an_x_and_y_scale == other.we_have_an_x_and_y_scale and
                self.we_have_a_two_by_two == other.we_have_a_two_by_two and
                self.we_have_instructions == other.we_have_instructions and
                self.use_my_metrics == other.use_my_metrics and
                self.overlap_compound == other.overlap_compound and
                self.scaled_component_offset == other.scaled_component_offset and
                self.unscaled_component_offset == other.unscaled_component_offset)

    @property
    def value(self) -> int:
        value = 0
        if self.arg_1_and_2_are_words:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_ARG_1_AND_2_ARE_WORDS
        if self.args_are_xy_values:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_ARGS_ARE_XY_VALUES
        if self.round_xy_to_grid:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_ROUND_XY_TO_GRID
        if self.we_have_a_scale:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_SCALE
        if self.more_components:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_MORE_COMPONENTS
        if self.we_have_an_x_and_y_scale:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_AN_X_AND_Y_SCALE
        if self.we_have_a_two_by_two:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_A_TWO_BY_TWO
        if self.we_have_instructions:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_WE_HAVE_INSTRUCTIONS
        if self.use_my_metrics:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_USE_MY_METRICS
        if self.overlap_compound:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_OVERLAP_COMPOUND
        if self.scaled_component_offset:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_SCALED_COMPONENT_OFFSET
        if self.unscaled_component_offset:
            value |= _COMPONENT_GLYPH_FLAGS_MASK_UNSCALED_COMPONENT_OFFSET
        return value

    def copy(self) -> ComponentGlyphFlags:
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


class XyGlyphComponent:
    glyph_index: int
    x: int
    y: int
    round_xy_to_grid: bool
    scaled_component_offset: bool
    unscaled_component_offset: bool
    transform: tuple[float, float, float, float]
    use_my_metrics: bool

    def __init__(
            self,
            glyph_index: int = 0,
            x: int = 0,
            y: int = 0,
            round_xy_to_grid: bool = False,
            scaled_component_offset: bool = False,
            unscaled_component_offset: bool = False,
            transform: tuple[float, float, float, float] = (0, 0, 0, 0),
            use_my_metrics: bool = False,
    ):
        self.glyph_index = glyph_index
        self.x = x
        self.y = y
        self.round_xy_to_grid = round_xy_to_grid
        self.scaled_component_offset = scaled_component_offset
        self.unscaled_component_offset = unscaled_component_offset
        self.transform = transform
        self.use_my_metrics = use_my_metrics

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, XyGlyphComponent):
            return False
        return (self.glyph_index == other.glyph_index and
                self.x == other.x and
                self.y == other.y and
                self.round_xy_to_grid == other.round_xy_to_grid and
                self.scaled_component_offset == other.scaled_component_offset and
                self.unscaled_component_offset == other.unscaled_component_offset and
                self.transform == other.transform and
                self.use_my_metrics == other.use_my_metrics)

    def copy(self) -> XyGlyphComponent:
        return XyGlyphComponent(
            self.glyph_index,
            self.x,
            self.y,
            self.round_xy_to_grid,
            self.scaled_component_offset,
            self.unscaled_component_offset,
            self.transform,
            self.use_my_metrics,
        )


class PointsGlyphComponent:
    glyph_index: int
    parent_point: int
    child_point: int
    transform: tuple[float, float, float, float] | None
    use_my_metrics: bool

    def __init__(
            self,
            glyph_index: int = 0,
            parent_point: int = 0,
            child_point: int = 0,
            transform: tuple[float, float, float, float] | None = None,
            use_my_metrics: bool = False,
    ):
        self.glyph_index = glyph_index
        self.parent_point = parent_point
        self.child_point = child_point
        self.transform = transform
        self.use_my_metrics = use_my_metrics

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, PointsGlyphComponent):
            return False
        return (self.glyph_index == other.glyph_index and
                self.parent_point == other.parent_point and
                self.child_point == other.child_point and
                self.transform == other.transform and
                self.use_my_metrics == other.use_my_metrics)

    def copy(self) -> PointsGlyphComponent:
        return PointsGlyphComponent(
            self.glyph_index,
            self.parent_point,
            self.child_point,
            self.transform,
            self.use_my_metrics,
        )


class ComponentGlyph:
    @staticmethod
    def parse_body(
            stream: Stream,
            x_min: int,
            y_min: int,
            x_max: int,
            y_max: int,
    ) -> ComponentGlyph:
        components = []
        overlap_compound = None
        we_have_instructions = False
        while True:
            flags = ComponentGlyphFlags.parse(stream.read_uint16())
            glyph_index = stream.read_uint16()

            if overlap_compound is None:
                overlap_compound = flags.overlap_compound

            if flags.arg_1_and_2_are_words:
                if flags.args_are_xy_values:
                    argument1 = stream.read_int16()
                    argument2 = stream.read_int16()
                else:
                    argument1 = stream.read_uint16()
                    argument2 = stream.read_uint16()
            else:
                if flags.args_are_xy_values:
                    argument1 = stream.read_int8()
                    argument2 = stream.read_int8()
                else:
                    argument1 = stream.read_uint8()
                    argument2 = stream.read_uint8()

            if flags.we_have_a_scale:
                scale = stream.read_f2dot14()
                transform = scale, 0, 0, scale
            elif flags.we_have_an_x_and_y_scale:
                x_scale = stream.read_f2dot14()
                y_scale = stream.read_f2dot14()
                transform = x_scale, 0, 0, y_scale
            elif flags.we_have_a_two_by_two:
                x_scale = stream.read_f2dot14()
                scale_01 = stream.read_f2dot14()
                scale_10 = stream.read_f2dot14()
                y_scale = stream.read_f2dot14()
                transform = x_scale, scale_01, scale_10, y_scale
            else:
                transform = None

            if flags.args_are_xy_values:
                components.append(XyGlyphComponent(
                    glyph_index,
                    argument1,
                    argument2,
                    flags.round_xy_to_grid,
                    flags.scaled_component_offset,
                    flags.unscaled_component_offset,
                    transform,
                    flags.use_my_metrics,
                ))
            else:
                components.append(PointsGlyphComponent(
                    glyph_index,
                    argument1,
                    argument2,
                    transform,
                    flags.use_my_metrics,
                ))

            if not flags.more_components:
                if flags.we_have_instructions:
                    we_have_instructions = True
                break

        if we_have_instructions:
            instruction_length = stream.read_uint16()
            instructions = stream.read(instruction_length)
        else:
            instructions = b''

        return ComponentGlyph(
            x_min,
            y_min,
            x_max,
            y_max,
            components,
            instructions,
            overlap_compound,
        )

    @staticmethod
    def parse(data: bytes) -> ComponentGlyph:
        stream = Stream(data)

        stream.read_int16()
        x_min = stream.read_int16()
        y_min = stream.read_int16()
        x_max = stream.read_int16()
        y_max = stream.read_int16()

        return ComponentGlyph.parse_body(stream, x_min, y_min, x_max, y_max)

    x_min: int
    y_min: int
    x_max: int
    y_max: int
    components: list[XyGlyphComponent | PointsGlyphComponent]
    instructions: bytes
    overlap_compound: bool

    def __init__(
            self,
            x_min: int = 0,
            y_min: int = 0,
            x_max: int = 0,
            y_max: int = 0,
            components: list[XyGlyphComponent | PointsGlyphComponent] | None = None,
            instructions: bytes = b'',
            overlap_compound: bool = False,
    ):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.components = [] if components is None else components
        self.instructions = instructions
        self.overlap_compound = overlap_compound

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, ComponentGlyph):
            return False
        return (self.x_min == other.x_min and
                self.y_min == other.y_min and
                self.x_max == other.x_max and
                self.y_max == other.y_max and
                self.components == other.components and
                self.instructions == other.instructions and
                self.overlap_compound == other.overlap_compound)

    @property
    def num_components(self) -> int:
        return len(self.components)

    def copy(self) -> ComponentGlyph:
        components = [component.copy() for component in self.components]
        return ComponentGlyph(
            self.x_min,
            self.y_min,
            self.x_max,
            self.y_max,
            components,
            self.instructions,
            self.overlap_compound,
        )

    def dump_body(self, stream: Stream):
        for i, component in enumerate(self.components):
            flags = ComponentGlyphFlags(
                more_components=True,
            )

            if i == 0:
                flags.overlap_compound = self.overlap_compound

            if i == self.num_components - 1:
                flags.more_components = False
                flags.we_have_instructions = len(self.instructions) > 0

            if isinstance(component, XyGlyphComponent):
                glyph_index = component.glyph_index
                argument1 = component.x
                argument2 = component.y
                transform = component.transform
                flags.args_are_xy_values = True
                flags.arg_1_and_2_are_words = argument1 > 0x7F and argument2 > 0x7F
                flags.round_xy_to_grid = component.round_xy_to_grid
                flags.scaled_component_offset = component.scaled_component_offset
                flags.unscaled_component_offset = component.unscaled_component_offset
                flags.use_my_metrics = component.use_my_metrics
            elif isinstance(component, PointsGlyphComponent):
                glyph_index = component.glyph_index
                argument1 = component.parent_point
                argument2 = component.child_point
                transform = component.transform
                flags.arg_1_and_2_are_words = argument1 > 0xFF and argument2 > 0xFF
                flags.use_my_metrics = component.use_my_metrics
            else:
                raise SfntError('[glyf] unknown glyph type')

            if transform is not None:
                x_scale, scale_01, scale_10, y_scale = transform
                if x_scale == y_scale and scale_01 == scale_10 == 0:
                    flags.we_have_a_scale = True
                elif scale_01 == scale_10 == 0:
                    flags.we_have_an_x_and_y_scale = True
                else:
                    flags.we_have_a_two_by_two = True

            stream.write_uint16(flags.value)
            stream.write_uint16(glyph_index)

            if flags.arg_1_and_2_are_words:
                if flags.args_are_xy_values:
                    stream.write_int16(argument1)
                    stream.write_int16(argument2)
                else:
                    stream.write_uint16(argument1)
                    stream.write_uint16(argument2)
            else:
                if flags.args_are_xy_values:
                    stream.write_int8(argument1)
                    stream.write_int8(argument2)
                else:
                    stream.write_uint8(argument1)
                    stream.write_uint8(argument2)

            if transform is not None:
                x_scale, scale_01, scale_10, y_scale = transform
                if flags.we_have_a_scale:
                    stream.write_f2dot14(x_scale)
                elif flags.we_have_an_x_and_y_scale:
                    stream.write_f2dot14(x_scale)
                    stream.write_f2dot14(y_scale)
                elif flags.we_have_a_two_by_two:
                    stream.write_f2dot14(x_scale)
                    stream.write_f2dot14(scale_01)
                    stream.write_f2dot14(scale_10)
                    stream.write_f2dot14(y_scale)

        if len(self.instructions) > 0:
            stream.write_uint16(len(self.instructions))
            stream.write(self.instructions)

    def dump(self) -> bytes:
        stream = Stream()

        stream.write_int16(-1)
        stream.write_int16(self.x_min)
        stream.write_int16(self.y_min)
        stream.write_int16(self.x_max)
        stream.write_int16(self.y_max)

        self.dump_body(stream)

        return stream.get_value()
