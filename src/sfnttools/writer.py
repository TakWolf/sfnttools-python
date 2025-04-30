from sfnttools.table import SfntTable, SfntTableContainer


class SfntWriter(SfntTableContainer):
    def get_table(self, tag: str) -> SfntTable:
        raise NotImplementedError()


class SfntCollectionWriter:
    pass
