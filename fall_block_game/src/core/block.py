from src.core.position import Position


class Block:
    """A block with rotation states and positioning.

    :param id: Unique identifier for the block type.
    :type id: int
    :param name: Name of the block (e.g., "T", "L", "J").
    :type name: str
    :param cells: A tuple of rotation states, each state is a tuple of Position objects
                representing the occupied cells relative to the block's origin.
    :type cells: tuple[tuple[Position, ...], ...]
    :param matrix_size: Size of the square matrix (e.g., 2 for 2x2, 3 for 3x3) used for collision detection.
    :type matrix_size: int
    :param wall_kicks: Wall kick data for each clockwise rotation state; a list of lists of [delta_row, delta_col] offsets.
    :type wall_kicks: list[list[list[int]]]
    """

    def __init__(
        self,
        id: int,
        name: str,
        cells: tuple[tuple[Position, ...], ...],
        matrix_size: int,
        wall_kicks: list[list[list[int]]],
    ):
        self._id: int = id
        self._name: str = name
        self._cells: tuple[tuple[Position, ...], ...] = cells
        self._matrix_size = matrix_size
        self._wall_kicks = wall_kicks
        self._rotation_state: int = 0
        self._row_offset: int = 0
        self._col_offset: int = 0

    @property
    def id(self) -> int:
        """Return the unique identifier of the block."""
        return self._id

    @property
    def name(self) -> str:
        """Return the name of the block."""
        return self._name

    @property
    def rotation_state(self) -> int:
        """Return the current rotation state index."""
        return self._rotation_state

    @property
    def row_offset(self) -> int:
        """Return the current row offset of the block."""
        return self._row_offset

    @property
    def col_offset(self) -> int:
        """Return the current column offset of the block."""
        return self._col_offset

    def move_to_spawn(self, grid_width: int) -> None:
        """Center the block horizontally at the top of the grid and adjust vertical position.

        The block is centered based on its matrix size and the grid width.

        :param grid_width: Total number of columns in the game grid.
        :type grid_width: int
        :return: None
        :rtype: None
        """

        self._col_offset = (grid_width - self._matrix_size) // 2

        self._row_offset = 0

        tiles = self._cells[self.rotation_state]
        is_top_row_empty = all(pos.row > 0 for pos in tiles)

        if is_top_row_empty:
            self._row_offset = -1

    def get_moved_positions(self, d_row: int, d_col: int) -> list[Position]:
        """Return positions after applying a relative move without changing actual block state.

        :param d_row: Number of rows to move (positive = down).
        :type d_row: int
        :param d_col: Number of columns to move (positive = right).
        :type d_col: int
        :return: List of Positions representing the block's cells after the move.
        :rtype: list[Position]
        """
        tiles = self._cells[self.rotation_state]
        return [
            Position(
                p.row + self.row_offset + d_row, p.column + self.col_offset + d_col
            )
            for p in tiles
        ]

    def get_rotated_positions(self, clockwise: bool = True) -> list[Position]:
        """Return positions after one rotation without changing actual block state.

        :param clockwise: If ``True``, rotate 90° clockwise; if ``False``, rotate 90° counter-clockwise.
        :type clockwise: bool
        :return: List of Positions for the next rotation state.
        :rtype: list[Position]
        """
        if clockwise:
            next_rotation = (self.rotation_state + 1) % len(self._cells)
        else:
            next_rotation = (self.rotation_state - 1) % len(self._cells)
        tiles = self._cells[next_rotation]
        return [
            Position(p.row + self.row_offset, p.column + self.col_offset) for p in tiles
        ]

    def get_rotated_and_moved_positions(
        self, d_row: int, d_col: int, clockwise: bool = True
    ) -> list[Position]:
        """Return positions after one rotation and a relative move without changing the actual block state.

        Computes the positions that the block would occupy if it were rotated
        (clockwise or counter-clockwise) and then shifted by the given row/column
        offsets, but does not modify the block's internal state.

        :param d_row: Number of rows to shift downward (positive) or upward (negative).
        :type d_row: int
        :param d_col: Number of columns to shift right (positive) or left (negative).
        :type d_col: int
        :param clockwise: If ``True``, rotate 90° clockwise; if ``False``, rotate 90° counter-clockwise.
        :type clockwise: bool
        :return: List of positions after the hypothetical rotation and movement.
        :rtype: list[Position]
        """
        if clockwise:
            next_rotation = (self.rotation_state + 1) % len(self._cells)
        else:
            next_rotation = (self.rotation_state - 1) % len(self._cells)
        tiles = self._cells[next_rotation]
        return [
            Position(
                p.row + self.row_offset + d_row, p.column + self.col_offset + d_col
            )
            for p in tiles
        ]

    def get_kick_translations(self, clockwise: bool = True) -> list[tuple[int, int]]:
        """
        Returns a list of kick offsets (dx, dy) to move from the current state to the next state.
        :param clockwise: If ``True``, rotate 90° clockwise; if ``False``, rotate 90° counter-clockwise.
        :type clockwise: bool
        :return: List of kick offsets (dx, dy)
        :rtype: list[tuple[int, int]]
        """
        if not self._wall_kicks:
            return [(0, 0)]
        if clockwise:
            new_state = (self._rotation_state + 1) % len(self._cells)

            return self._wall_kicks[new_state]
        else:
            cw_kicks = self._wall_kicks[self._rotation_state]

            return [(-dx, -dy) for dx, dy in cw_kicks]

    def rotate(self, clockwise: bool = True) -> None:
        """Rotate the block by advancing to the next rotation state.
        :param clockwise: If ``True``, rotate 90° clockwise; if ``False``, rotate 90° counter-clockwise.
        :type clockwise: bool
        :return: None
        :rtype: None
        """
        if clockwise:
            self._rotation_state = (self._rotation_state + 1) % len(self._cells)
        else:
            self._rotation_state = (self._rotation_state - 1) % len(self._cells)

    def move(self, rows: int, columns: int) -> None:
        """Move the block by a given offset.

        :param rows: Number of rows to shift (positive = down).
        :type rows: int
        :param columns: Number of columns to shift (positive = right).
        :type columns: int
        :return: None
        :rtype: None
        """
        self._row_offset += rows
        self._col_offset += columns

    def get_cell_positions(self) -> list[Position]:
        """Return the absolute positions of all cells in the current block state.

        :return: List of Positions representing occupied cells.
        :rtype: list[Position]
        """
        tiles: list[Position] = self._cells[self._rotation_state]

        return [
            Position(pos.row + self.row_offset, pos.column + self.col_offset)
            for pos in tiles
        ]
