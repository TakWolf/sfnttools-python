from typing import Any

from sfnttools.flags import SfntFlags

_HEAD_TABLE_FLAGS_MASK_BASELINE_AT_Y0 = 0b_0000_0000_0000_0001
_HEAD_TABLE_FLAGS_MASK_LEFT_SIDEBEARING_AT_X0 = 0b_0000_0000_0000_0010
_HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_DEPEND_ON_POINT_SIZE = 0b_0000_0000_0000_0100
_HEAD_TABLE_FLAGS_MASK_FORCE_PPEM_TO_INTEGER = 0b_0000_0000_0000_1000
_HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_ALTER_ADVANCE_WIDTH = 0b_0000_0000_0001_0000
_HEAD_TABLE_FLAGS_MASK_FONT_DATA_IS_LOSSLESS_AFTER_OPTIMIZATION = 0b_0000_1000_0000_0000
_HEAD_TABLE_FLAGS_MASK_FONT_CONVERTED = 0b_0001_0000_0000_0000
_HEAD_TABLE_FLAGS_MASK_FONT_OPTIMIZED_FOR_CLEARTYPE = 0b_0010_0000_0000_0000
_HEAD_TABLE_FLAGS_MASK_LAST_RESORT_FONT = 0b_0100_0000_0000_0000

_MAC_STYLE_MASK_BOLD = 0b_0000_0000_0000_0001
_MAC_STYLE_MASK_ITALIC = 0b_0000_0000_0000_0010
_MAC_STYLE_MASK_UNDERLINE = 0b_0000_0000_0000_0100
_MAC_STYLE_MASK_OUTLINE = 0b_0000_0000_0000_1000
_MAC_STYLE_MASK_SHADOW = 0b_0000_0000_0001_0000
_MAC_STYLE_MASK_CONDENSED = 0b_0000_0000_0010_0000
_MAC_STYLE_MASK_EXTENDED = 0b_0000_0000_0100_0000


class HeadTableFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'HeadTableFlags':
        baseline_at_y0 = value & _HEAD_TABLE_FLAGS_MASK_BASELINE_AT_Y0 > 0
        left_sidebearing_at_x0 = value & _HEAD_TABLE_FLAGS_MASK_LEFT_SIDEBEARING_AT_X0 > 0
        instructions_may_depend_on_point_size = value & _HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_DEPEND_ON_POINT_SIZE > 0
        force_ppem_to_integer = value & _HEAD_TABLE_FLAGS_MASK_FORCE_PPEM_TO_INTEGER > 0
        instructions_may_alter_advance_width = value & _HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_ALTER_ADVANCE_WIDTH > 0
        font_data_is_lossless_after_optimization = value & _HEAD_TABLE_FLAGS_MASK_FONT_DATA_IS_LOSSLESS_AFTER_OPTIMIZATION > 0
        font_converted = value & _HEAD_TABLE_FLAGS_MASK_FONT_CONVERTED > 0
        font_optimized_for_cleartype = value & _HEAD_TABLE_FLAGS_MASK_FONT_OPTIMIZED_FOR_CLEARTYPE > 0
        last_resort_font = value & _HEAD_TABLE_FLAGS_MASK_LAST_RESORT_FONT > 0
        return HeadTableFlags(
            baseline_at_y0,
            left_sidebearing_at_x0,
            instructions_may_depend_on_point_size,
            force_ppem_to_integer,
            instructions_may_alter_advance_width,
            font_data_is_lossless_after_optimization,
            font_converted,
            font_optimized_for_cleartype,
            last_resort_font,
        )

    baseline_at_y0: bool
    left_sidebearing_at_x0: bool
    instructions_may_depend_on_point_size: bool
    force_ppem_to_integer: bool
    instructions_may_alter_advance_width: bool
    font_data_is_lossless_after_optimization: bool
    font_converted: bool
    font_optimized_for_cleartype: bool
    last_resort_font: bool

    def __init__(
            self,
            baseline_at_y0: bool = False,
            left_sidebearing_at_x0: bool = False,
            instructions_may_depend_on_point_size: bool = False,
            force_ppem_to_integer: bool = False,
            instructions_may_alter_advance_width: bool = False,
            font_data_is_lossless_after_optimization: bool = False,
            font_converted: bool = False,
            font_optimized_for_cleartype: bool = False,
            last_resort_font: bool = False,
    ):
        self.baseline_at_y0 = baseline_at_y0
        self.left_sidebearing_at_x0 = left_sidebearing_at_x0
        self.instructions_may_depend_on_point_size = instructions_may_depend_on_point_size
        self.force_ppem_to_integer = force_ppem_to_integer
        self.instructions_may_alter_advance_width = instructions_may_alter_advance_width
        self.font_data_is_lossless_after_optimization = font_data_is_lossless_after_optimization
        self.font_converted = font_converted
        self.font_optimized_for_cleartype = font_optimized_for_cleartype
        self.last_resort_font = last_resort_font

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HeadTableFlags):
            return False
        return (self.baseline_at_y0 == other.baseline_at_y0 and
                self.left_sidebearing_at_x0 == other.left_sidebearing_at_x0 and
                self.instructions_may_depend_on_point_size == other.instructions_may_depend_on_point_size and
                self.force_ppem_to_integer == other.force_ppem_to_integer and
                self.instructions_may_alter_advance_width == other.instructions_may_alter_advance_width and
                self.font_data_is_lossless_after_optimization == other.font_data_is_lossless_after_optimization and
                self.font_converted == other.font_converted and
                self.font_optimized_for_cleartype == other.font_optimized_for_cleartype and
                self.last_resort_font == other.last_resort_font)

    @property
    def value(self) -> int:
        value = 0
        if self.baseline_at_y0:
            value |= _HEAD_TABLE_FLAGS_MASK_BASELINE_AT_Y0
        if self.left_sidebearing_at_x0:
            value |= _HEAD_TABLE_FLAGS_MASK_LEFT_SIDEBEARING_AT_X0
        if self.instructions_may_depend_on_point_size:
            value |= _HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_DEPEND_ON_POINT_SIZE
        if self.force_ppem_to_integer:
            value |= _HEAD_TABLE_FLAGS_MASK_FORCE_PPEM_TO_INTEGER
        if self.instructions_may_alter_advance_width:
            value |= _HEAD_TABLE_FLAGS_MASK_INSTRUCTIONS_MAY_ALTER_ADVANCE_WIDTH
        if self.font_data_is_lossless_after_optimization:
            value |= _HEAD_TABLE_FLAGS_MASK_FONT_DATA_IS_LOSSLESS_AFTER_OPTIMIZATION
        if self.font_converted:
            value |= _HEAD_TABLE_FLAGS_MASK_FONT_CONVERTED
        if self.font_optimized_for_cleartype:
            value |= _HEAD_TABLE_FLAGS_MASK_FONT_OPTIMIZED_FOR_CLEARTYPE
        if self.last_resort_font:
            value |= _HEAD_TABLE_FLAGS_MASK_LAST_RESORT_FONT
        return value

    def copy(self) -> 'HeadTableFlags':
        return HeadTableFlags(
            self.baseline_at_y0,
            self.left_sidebearing_at_x0,
            self.instructions_may_depend_on_point_size,
            self.force_ppem_to_integer,
            self.instructions_may_alter_advance_width,
            self.font_data_is_lossless_after_optimization,
            self.font_converted,
            self.font_optimized_for_cleartype,
            self.last_resort_font,
        )


class MacStyle(SfntFlags):
    @staticmethod
    def parse(value: int) -> 'MacStyle':
        bold = value & _MAC_STYLE_MASK_BOLD > 0
        italic = value & _MAC_STYLE_MASK_ITALIC > 0
        underline = value & _MAC_STYLE_MASK_UNDERLINE > 0
        outline = value & _MAC_STYLE_MASK_OUTLINE > 0
        shadow = value & _MAC_STYLE_MASK_SHADOW > 0
        condensed = value & _MAC_STYLE_MASK_CONDENSED > 0
        extended = value & _MAC_STYLE_MASK_EXTENDED > 0
        return MacStyle(
            bold,
            italic,
            underline,
            outline,
            shadow,
            condensed,
            extended,
        )

    bold: bool
    italic: bool
    underline: bool
    outline: bool
    shadow: bool
    condensed: bool
    extended: bool

    def __init__(
            self,
            bold: bool = False,
            italic: bool = False,
            underline: bool = False,
            outline: bool = False,
            shadow: bool = False,
            condensed: bool = False,
            extended: bool = False,
    ):
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.outline = outline
        self.shadow = shadow
        self.condensed = condensed
        self.extended = extended

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, MacStyle):
            return False
        return (self.bold == other.bold and
                self.italic == other.italic and
                self.underline == other.underline and
                self.outline == other.outline and
                self.shadow == other.shadow and
                self.condensed == other.condensed and
                self.extended == other.extended)

    @property
    def value(self) -> int:
        value = 0
        if self.bold:
            value |= _MAC_STYLE_MASK_BOLD
        if self.italic:
            value |= _MAC_STYLE_MASK_ITALIC
        if self.underline:
            value |= _MAC_STYLE_MASK_UNDERLINE
        if self.outline:
            value |= _MAC_STYLE_MASK_OUTLINE
        if self.shadow:
            value |= _MAC_STYLE_MASK_SHADOW
        if self.condensed:
            value |= _MAC_STYLE_MASK_CONDENSED
        if self.extended:
            value |= _MAC_STYLE_MASK_EXTENDED
        return value

    def copy(self) -> 'MacStyle':
        return MacStyle(
            self.bold,
            self.italic,
            self.underline,
            self.outline,
            self.shadow,
            self.condensed,
            self.extended,
        )
