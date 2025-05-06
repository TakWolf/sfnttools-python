from fontTools.ttLib import TTFont

from examples import assets_dir
from sfnttools.font import SfntFont, SfntFontCollection


def main():
    ts1 = TTFont(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.ttf'))
    ts1_glyf = ts1['glyf']
    for glyph_name in ts1_glyf.glyphs:
        ts1_glyf[glyph_name]
    ts2 = TTFont(assets_dir.joinpath('demo', 'demo.ttf'))
    ts2_glyf = ts2['glyf']
    for glyph_name in ts2_glyf.glyphs:
        ts2_glyf[glyph_name]
        
    s1 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.otf'), verify_checksum=False)
    # s2 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.otf.woff2'), verify_checksum=False)
    s3 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.ttf'), verify_checksum=False)
    # s4 = SfntFont.load(assets_dir.joinpath('source-han-sans', 'SourceHanSansSC-VF.ttf.woff2'), verify_checksum=False)
    s5 = SfntFontCollection.load(assets_dir.joinpath('source-han-sans', 'SourceHanSans-VF.otf.ttc'), verify_checksum=False)
    s6 = SfntFontCollection.load(assets_dir.joinpath('source-han-sans', 'SourceHanSans-VF.ttf.ttc'), verify_checksum=False)

    d1 = SfntFont.load(assets_dir.joinpath('demo', 'demo.otf'), verify_checksum=False)
    d2 = SfntFont.load(assets_dir.joinpath('demo', 'demo.otf.woff'), verify_checksum=False)
    # d3 = SfntFont.load(assets_dir.joinpath('demo', 'demo.otf.woff2'), verify_checksum=False)
    d4 = SfntFont.load(assets_dir.joinpath('demo', 'demo.ttf'), verify_checksum=False)
    d5 = SfntFont.load(assets_dir.joinpath('demo', 'demo.ttf.woff'), verify_checksum=False)
    # d6 = SfntFont.load(assets_dir.joinpath('demo', 'demo.ttf.woff2'), verify_checksum=False)
    d7 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.otc'), verify_checksum=False)
    # d8 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.otc.woff2'), verify_checksum=False)
    d9 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.ttc'), verify_checksum=False)
    # d10 = SfntFontCollection.load(assets_dir.joinpath('demo', 'demo.ttc.woff2'), verify_checksum=False)

    print()


if __name__ == '__main__':
    main()
