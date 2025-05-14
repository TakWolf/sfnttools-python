from datetime import datetime, timezone

_TIMESTAMP_1904 = int(datetime(1904, 1, 1, tzinfo=timezone.utc).timestamp())


def seconds_since_1904_to_timestamp(value: int) -> int:
    return value + _TIMESTAMP_1904


def timestamp_to_seconds_since_1904(value: int) -> int:
    return value - _TIMESTAMP_1904
