from sfnttools.table import SfntTableWriter, SfntTable


class SfntWriter(SfntTableWriter):
    def get_table(self, tag: str, readonly: bool = True) -> SfntTable:
        pass

    def replace_table(self, tag: str, table: SfntTable):
        pass


class SfntCollectionWriter:
    pass
