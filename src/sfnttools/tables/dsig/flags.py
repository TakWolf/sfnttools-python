from __future__ import annotations

from typing import Any

from sfnttools.flags import SfntFlags

_DSIG_PERMISSION_FLAGS_MASK_CANNOT_BE_RESIGNED = 0b_0000_0000_0000_0001


class DsigPermissionFlags(SfntFlags):
    @staticmethod
    def parse(value: int) -> DsigPermissionFlags:
        cannot_be_resigned = value & _DSIG_PERMISSION_FLAGS_MASK_CANNOT_BE_RESIGNED > 0
        return DsigPermissionFlags(cannot_be_resigned)

    cannot_be_resigned: bool

    def __init__(self, cannot_be_resigned: bool = False):
        self.cannot_be_resigned = cannot_be_resigned

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DsigPermissionFlags):
            return NotImplemented
        return self.cannot_be_resigned == other.cannot_be_resigned

    @property
    def value(self) -> int:
        value = 0
        if self.cannot_be_resigned:
            value |= _DSIG_PERMISSION_FLAGS_MASK_CANNOT_BE_RESIGNED
        return value

    def copy(self) -> DsigPermissionFlags:
        return DsigPermissionFlags(self.cannot_be_resigned)
