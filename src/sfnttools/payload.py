from sfnttools.tables.dsig import DsigTable


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
