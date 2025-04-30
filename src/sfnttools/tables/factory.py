from typing import Final

from sfnttools.tables.default import DefaultTable
from sfnttools.tables.dsig import DsigTable
from sfnttools.tables.head import HeadTable

TABLE_TYPE_REGISTRY: Final = {
    'DSIG': DsigTable,
    'head': HeadTable,
}

DEFAULT_TABLE_TYPE: Final = DefaultTable
