from dataclasses import dataclass


@dataclass
class Position:
    """A 2D position on the grid with row and column coordinates.

    :param row: The row index (0-based, increasing downward).
    :type row: int
    :param column: The column index (0-based, increasing rightward).
    :type column: int
    """

    row: int
    column: int
