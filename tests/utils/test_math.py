from sfnttools.utils.math import round_half_up


def test_round_half_up():
    assert round_half_up(1.4) == 1
    assert round_half_up(1.5) == 2
    assert round_half_up(1.6) == 2
    assert round_half_up(2.4) == 2
    assert round_half_up(2.5) == 3
    assert round_half_up(2.6) == 3
    assert round_half_up(3.4) == 3
    assert round_half_up(3.5) == 4
    assert round_half_up(3.6) == 4
    assert round_half_up(4.4) == 4
    assert round_half_up(4.5) == 5
    assert round_half_up(4.6) == 5

    assert round_half_up(-1.4) == -1
    assert round_half_up(-1.5) == -2
    assert round_half_up(-1.6) == -2
    assert round_half_up(-2.4) == -2
    assert round_half_up(-2.5) == -3
    assert round_half_up(-2.6) == -3
    assert round_half_up(-3.4) == -3
    assert round_half_up(-3.5) == -4
    assert round_half_up(-3.6) == -4
    assert round_half_up(-4.4) == -4
    assert round_half_up(-4.5) == -5
    assert round_half_up(-4.6) == -5

    assert round_half_up(1.2445, 2) == 1.24
    assert round_half_up(1.2455, 2) == 1.25
    assert round_half_up(1.2465, 2) == 1.25

    assert round_half_up(-1.2445, 2) == -1.24
    assert round_half_up(-1.2455, 2) == -1.25
    assert round_half_up(-1.2465, 2) == -1.25
