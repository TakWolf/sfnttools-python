from pathlib import Path

from sfnttools.font import SfntFont


def test(assets_dir: Path):
    s1 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.otf'), verify_checksum=True)
    s1.pop('DSIG')
    s1.pop('head')
    s2 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.otf.woff2'), verify_checksum=True)
    s2.pop('head')
    s2.woff_payload = None
    for tag in s1.keys():
        table1 = s1[tag]
        table2 = s2[tag]
        assert table1 == table2


