from sfnttools.utils.time import seconds_since_1904_to_timestamp, timestamp_to_seconds_since_1904


def test_convert():
    assert seconds_since_1904_to_timestamp(3786912000) == 1704067200
    assert timestamp_to_seconds_since_1904(1704067200) == 3786912000
