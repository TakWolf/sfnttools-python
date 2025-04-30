from enum import StrEnum


class SfntVersion(StrEnum):
    TRUE_TYPE = '\x00\x01\x00\x00'
    OPEN_TYPE = 'OTTO'
    MACOS_TRUE_TYPE = 'true'
    MACOS_TYPE_1 = 'typ1'


class SfntFileTag(StrEnum):
    TTCF = 'ttcf'
    WOFF = 'wOFF'
    WOFF2 = 'wOF2'
