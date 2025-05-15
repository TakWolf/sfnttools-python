from typing import Final

from sfnttools.tables.default import DefaultTable
from sfnttools.tables.dsig.table import DsigTable
from sfnttools.tables.glyf.table import GlyfTable
from sfnttools.tables.head.table import HeadTable
from sfnttools.tables.hhea.table import HheaTable
from sfnttools.tables.hmtx.table import HmtxTable
from sfnttools.tables.loca.table import LocaTable
from sfnttools.tables.maxp.table import MaxpTable

TABLE_TYPE_REGISTRY: Final = {
    'DSIG': DsigTable,
    'glyf': GlyfTable,
    'head': HeadTable,
    'hhea': HheaTable,
    'hmtx': HmtxTable,
    'loca': LocaTable,
    'maxp': MaxpTable,
}

DEFAULT_TABLE_TYPE: Final = DefaultTable
