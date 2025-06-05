from __future__ import annotations

from typing import Any

from sfnttools.tables.dsig.table import DsigTable


class TtcPayload:
    major_version: int
    minor_version: int
    dsig_table: DsigTable | None

    def __init__(
            self,
            major_version: int = 1,
            minor_version: int = 0,
            dsig_table: DsigTable | None = None,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.dsig_table = dsig_table

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, TtcPayload):
            return NotImplemented
        return (self.major_version == other.major_version and
                self.minor_version == other.minor_version and
                self.dsig_table == other.dsig_table)

    def copy(self) -> TtcPayload:
        return TtcPayload(
            self.major_version,
            self.minor_version,
            self.dsig_table.copy(),
        )


class WoffPayload:
    major_version: int
    minor_version: int
    metadata: bytes | None
    private_data: bytes | None

    def __init__(
            self,
            major_version: int = 0,
            minor_version: int = 0,
            metadata: bytes | None = None,
            private_data: bytes | None = None,
    ):
        self.major_version = major_version
        self.minor_version = minor_version
        self.metadata = metadata
        self.private_data = private_data

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, WoffPayload):
            return NotImplemented
        return (self.major_version == other.major_version and
                self.minor_version == other.minor_version and
                self.metadata == other.metadata and
                self.private_data == other.private_data)

    def copy(self) -> WoffPayload:
        return WoffPayload(
            self.major_version,
            self.minor_version,
            self.metadata,
            self.private_data,
        )
