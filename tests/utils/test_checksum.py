from sfnttools.utils.checksum import calculate_checksum, calculate_checksum_adjustment


def test_calculate_checksum():
    assert calculate_checksum(b'abcd') == 1633837924
    assert calculate_checksum(b'abcdxyz') == 3655064932
    assert calculate_checksum(b'Hello World!') == 703735804


def test_calculate_checksum_adjustment():
    assert calculate_checksum_adjustment([
        1633837924,
        3655064932,
        703735804,
    ]) == 1283475190
