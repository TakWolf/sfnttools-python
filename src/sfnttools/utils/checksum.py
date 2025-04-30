
_CHECKSUM_MASK = 0xFFFFFFFF
_CHECKSUM_MAGIC_NUMBER = 0xB1B0AFBA


def calculate_checksum(data: bytes) -> int:
    checksum = 0
    for i in range(0, len(data), 4):
        chunk = data[i:i + 4]
        if len(chunk) < 4:
            chunk += b'\x00' * (4 - len(chunk))
        checksum += int.from_bytes(chunk, 'big', signed=False)
    checksum &= _CHECKSUM_MASK
    return checksum


def calculate_checksum_adjustment(checksums: list[int]) -> int:
    total_checksum = sum(checksums) & _CHECKSUM_MASK
    checksum_adjustment = (_CHECKSUM_MAGIC_NUMBER - total_checksum) & _CHECKSUM_MASK
    return checksum_adjustment
