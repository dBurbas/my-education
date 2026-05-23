from src.core.exception import GridError, GridCellError


class Grid:
    """A grid representing the game playfield.

    :param rows: Number of rows in the grid (default 20).
    :type rows: int
    :param columns: Number of columns in the grid (default 10).
    :type columns: int
    :raises GridError: If rows or columns are less than 1.
    """

    def __init__(self, rows: int = 20, columns: int = 10):
        if rows < 1 or columns < 1:
            raise GridError("Incorrect values for grid. Expected row > 1,column > 1")
        self._num_rows = rows
        self._num_cols = columns

        self._matrix: list[list[int]] = [
            [0 for _ in range(self._num_cols)] for _ in range(self._num_rows)
        ]
        self._color_name: str = "grid"

    @property
    def rows(self) -> int:
        """Return the number of rows in the grid."""
        return self._num_rows

    @property
    def cols(self) -> int:
        """Return the number of columns in the grid."""
        return self._num_cols

    def set_cell(self, row: int, column: int, value: int) -> None:
        """Set a cell's value at the given coordinates.

        :param row: Row index (0-based).
        :type row: int
        :param column: Column index (0-based).
        :type column: int
        :param value: Value to assign to the cell.
        :type value: int
        :raises GridCellError: If the coordinates are outside grid bounds.
        """
        if row < 0 or column < 0 or row >= self.rows or column >= self.cols:
            raise GridCellError(row, column, value, self._num_rows, self._num_cols)
        self._matrix[row][column] = value

    def is_inside(self, row: int, column: int) -> bool:
        """Check if given coordinates are inside the grid.

        :param row: Row index (0-based).
        :type row: int
        :param column: Column index (0-based).
        :type column: int
        :return: ``True`` if inside bounds, ``False`` otherwise.
        :rtype: bool
        """
        if (
            row >= 0
            and row < self._num_rows
            and column >= 0
            and column < self._num_cols
        ):
            return True
        return False

    def is_cell_empty(self, row: int, column: int) -> bool:
        """Check if a cell is empty (value == 0).

        :param row: Row index (0-based).
        :type row: int
        :param column: Column index (0-based).
        :type column: int
        :return: ``True`` if cell value is 0, ``False`` otherwise.
        :rtype: bool
        """
        return self._matrix[row][column] == 0

    def is_row_full(self, row: int) -> bool:
        """Check if a row contains no empty cells (all values ≠ 0).

        :param row: Row index (0-based).
        :type row: int
        :return: ``True`` if every cell in the row is non-zero, ``False`` otherwise.
        :rtype: bool
        """
        return 0 not in self._matrix[row]

    def reset(self) -> None:
        """Reset the grid to all zeros (clear all cells)."""
        self._matrix = [
            [0 for _ in range(self._num_cols)] for _ in range(self._num_rows)
        ]

    def clear_full_rows(self) -> tuple[int, list]:
        """Remove all completely filled rows and shift the rows above down.

        :return: Tuple containing number of rows cleared and their original indexes.
        """

        full_rows = []
        for row in range(self._num_rows):
            if 0 not in self._matrix[row]:
                full_rows.append(row)

        if not full_rows:
            return 0, []

        for row in reversed(full_rows):
            del self._matrix[row]

        for _ in range(len(full_rows)):
            self._matrix.insert(0, [0 for _ in range(self._num_cols)])

        return len(full_rows), full_rows
