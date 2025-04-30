from sfnttools.table import SfntTableContainer, SfntTable


class SfntWriter(SfntTableContainer):
    def get_table(self, tag: str) -> SfntTable:
        raise NotImplementedError()


class SfntCollectionWriter:
    pass
