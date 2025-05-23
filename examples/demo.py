from examples import assets_dir
from sfnttools.font import SfntFont, SfntFontCollection


def main():
    r1 = SfntFont.load(assets_dir.joinpath('retro-pixel', 'retro-pixel-cute-mono.ttf'), verify_checksum=True)
    r2 = SfntFont.load(assets_dir.joinpath('retro-pixel', 'retro-pixel-cute-mono.woff2'), verify_checksum=True)

    u1 = SfntFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.03.otf'), verify_checksum=True)
    u2 = SfntFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.03.otf.woff2'), verify_checksum=True)
    u3 = SfntFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.03.ttf'), verify_checksum=True)
    u4 = SfntFont.load(assets_dir.joinpath('unifont', 'unifont-16.0.03.ttf.woff2'), verify_checksum=True)

    g1 = SfntFont.load(assets_dir.joinpath('gulim', 'Gulim.ttf'), verify_checksum=True)
    g2 = SfntFont.load(assets_dir.joinpath('gulim', 'Gulim.woff2'), verify_checksum=True)
    g3 = SfntFont.load(assets_dir.joinpath('gulim', 'GulimChe.ttf'), verify_checksum=True)
    g4 = SfntFont.load(assets_dir.joinpath('gulim', 'GulimChe.woff2'), verify_checksum=True)
    g5 = SfntFont.load(assets_dir.joinpath('gulim', 'Dotum.ttf'), verify_checksum=True)
    g6 = SfntFont.load(assets_dir.joinpath('gulim', 'Dotum.woff2'), verify_checksum=True)
    g7 = SfntFont.load(assets_dir.joinpath('gulim', 'DotumChe.ttf'), verify_checksum=True)
    g8 = SfntFont.load(assets_dir.joinpath('gulim', 'DotumChe.woff2'), verify_checksum=True)
    g9 = SfntFontCollection.load(assets_dir.joinpath('gulim', 'gulim.ttc'), verify_checksum=True)

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
