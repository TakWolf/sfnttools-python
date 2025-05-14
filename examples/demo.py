from fontTools.ttLib import TTFont

from examples import assets_dir
from sfnttools.font import SfntFont, SfntFontCollection


def main():
    g1 = SfntFont.load(assets_dir.joinpath('gulim', 'Gulim.ttf'), verify_checksum=True)
    g2 = SfntFont.load(assets_dir.joinpath('gulim', 'GulimChe.ttf'), verify_checksum=True)
    g3 = SfntFont.load(assets_dir.joinpath('gulim', 'Dotum.ttf'), verify_checksum=True)
    g4 = SfntFont.load(assets_dir.joinpath('gulim', 'DotumChe.ttf'), verify_checksum=True)
    g5 = SfntFontCollection.load(assets_dir.joinpath('gulim', 'gulim.ttc'), verify_checksum=True)

    s1 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.otf'), verify_checksum=True)
    s2 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.otf.woff2'), verify_checksum=True)
    s3 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.ttf'), verify_checksum=True)
    s4 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.ttf.woff2'), verify_checksum=True)
    s5 = SfntFontCollection.load(assets_dir.joinpath('source-han-sans', 'SourceHanSans-VF.otf.ttc'), verify_checksum=True)
    s6 = SfntFontCollection.load(assets_dir.joinpath('source-han-sans', 'SourceHanSans-VF.ttf.ttc'), verify_checksum=True)

    d1 = SfntFont.load(assets_dir.joinpath('demo', 'demo.otf'), verify_checksum=True)
    d2 = SfntFont.load(assets_dir.joinpath('demo', 'demo.otf.woff'), verify_checksum=True)
    d3 = SfntFont.load(assets_dir.joinpath('demo', 'demo.otf.woff2'), verify_checksum=True)
    d4 = SfntFont.load(assets_dir.joinpath('demo', 'demo.ttf'), verify_checksum=True)
    d5 = SfntFont.load(assets_dir.joinpath('demo', 'demo.ttf.woff'), verify_checksum=True)
    d6 = SfntFont.load(assets_dir.joinpath('demo', 'demo.ttf.woff2'), verify_checksum=True)
    d7 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.otc'), verify_checksum=True)
    d8 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.otc.woff2'), verify_checksum=True)
    d9 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.ttc'), verify_checksum=True)
    d10 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.ttc.woff2'), verify_checksum=True)

    print()


if __name__ == '__main__':
    main()
