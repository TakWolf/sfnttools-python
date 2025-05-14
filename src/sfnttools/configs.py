from enum import IntEnum


class GlyfDataOffsetsPaddingMode(IntEnum):
    NO_PADDING = 0
    ALIGN_TO_2_BYTE = 2
    ALIGN_TO_4_BYTE = 4


class SfntConfigs:
    glyf_data_offsets_padding_mode: GlyfDataOffsetsPaddingMode

    def __init__(
            self,
            glyf_data_offsets_padding_mode: GlyfDataOffsetsPaddingMode = GlyfDataOffsetsPaddingMode.ALIGN_TO_2_BYTE,
    ):
        self.glyf_data_offsets_padding_mode = glyf_data_offsets_padding_mode
