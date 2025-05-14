from enum import IntEnum


class FontDirectionHint(IntEnum):
    FULLY_MIXED = 0
    LEFT_TO_RIGHT = 1
    LEFT_TO_RIGHT_CONTAINS_NEUTRALS = 2
    RIGHT_TO_LEFT = -1
    RIGHT_TO_LEFT_CONTAINS_NEUTRALS = -2


class IndexToLocFormat(IntEnum):
    SHORT = 0
    LONG = 1


class GlyphDataFormat(IntEnum):
    CURRENT = 0
