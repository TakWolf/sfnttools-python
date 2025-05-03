from typing import Final

from sfnttools.tables.default import DefaultTable
from sfnttools.tables.dsig import DsigTable
from sfnttools.tables.glyf import GlyfTable
from sfnttools.tables.head import HeadTable
from sfnttools.tables.loca import LocaTable
from sfnttools.tables.maxp import MaxpTable

TABLE_TYPE_REGISTRY: Final = {
    'DSIG': DsigTable,
    'glyf': GlyfTable,
    'head': HeadTable,
    'loca': LocaTable,
    'maxp': MaxpTable,
}

DEFAULT_TABLE_TYPE: Final = DefaultTable
