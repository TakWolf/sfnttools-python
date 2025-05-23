from typing import Final

from sfnttools.tables.cff2.table import Cff2Table
from sfnttools.tables.cff_.table import CffTable
from sfnttools.tables.default import DefaultTable
from sfnttools.tables.dsig.table import DsigTable
from sfnttools.tables.glyf.table import GlyfTable
from sfnttools.tables.head.table import HeadTable
from sfnttools.tables.hhea.table import HheaTable
from sfnttools.tables.hmtx.table import HmtxTable
from sfnttools.tables.loca.table import LocaTable
from sfnttools.tables.maxp.table import MaxpTable
from sfnttools.tables.vhea.table import VheaTable
from sfnttools.tables.vmtx.table import VmtxTable

TABLE_TYPE_REGISTRY: Final = {
    'CFF ': CffTable,
    'CFF2': Cff2Table,
    'DSIG': DsigTable,
    'glyf': GlyfTable,
    'head': HeadTable,
    'hhea': HheaTable,
    'hmtx': HmtxTable,
    'loca': LocaTable,
    'maxp': MaxpTable,
    'vhea': VheaTable,
    'vmtx': VmtxTable,
}

DEFAULT_TABLE_TYPE: Final = DefaultTable
