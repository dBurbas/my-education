import pytest
from src.core.base import Position


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0, 0, 0.0),
        (0, 3, 3.0),
        (4, 0, 4.0),
        (4, 4, 5.7),
    ],
)
def test_from_zero_position(x, y, expected):
    pos1: Position = Position(0, 0)
    pos2: Position = Position(x, y)
    assert round(pos1.distance_to(pos2), 1) == expected


@pytest.mark.parametrize(
    "x,y,expected",
    [
        (0, 0, 7.1),
        (0, 3, 5.4),
        (4, 0, 5.1),
        (4, 4, 1.4),
    ],
)
def test_from_non_zero_position(x, y, expected):
    pos1: Position = Position(5, 5)
    pos2: Position = Position(x, y)
    print(f"{round(pos1.distance_to(pos2), 1)} и {pos1.distance_to(pos2)}")
    assert round(pos1.distance_to(pos2), 1) == expected
