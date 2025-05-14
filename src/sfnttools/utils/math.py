import math


def round_half_up(value: int | float, n_digits: int = 0) -> int | float:
    positive = value >= 0
    shift = 10 ** n_digits
    value = math.floor(abs(value * shift) + 0.5) / shift
    if not positive:
        value *= -1
    if n_digits == 0:
        value = int(value)
    return value
