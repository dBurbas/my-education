from src.core.position import Position


class Block:
    """A block with rotation states and positioning.

    :param block_data: Dictionary containing block information with keys:
                       "id" (int), "name" (str, optional), "states" (list of 2D matrices)
    :type block_data: dict
    """

    def __init__(self, block_data: dict):
        self._id: int = block_data["id"]
        self._name: str = block_data.get("name", "Unknown")
        self._cells: tuple[tuple[Position, ...], ...] = self._parse_states(
            block_data["states"]
        )
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

    def _parse_states(
        self, states_matrices: list[list[list[int]]]
    ) -> tuple[tuple[Position, ...], ...]:
        """Convert rotation matrices into immutable tuples of cell positions.

        :param states_matrices: List of 2D matrices (rows x columns) with 1 representing a cell.
        :type states_matrices: list[list[list[int]]]
        :return: Tuple where each element is a tuple of Positions for that rotation state.
        :rtype: tuple[tuple[Position, ...], ...]
        """
        parsed_states = []
        for matrix in states_matrices:
            positions = []
            for row_idx, row in enumerate(matrix):
                for col_idx, val in enumerate(row):
                    if val == 1:
                        positions.append(Position(row_idx, col_idx))
            parsed_states.append(tuple(positions))
        return tuple(parsed_states)

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

    def get_rotated_positions(self) -> list[Position]:
        """Return positions after one clockwise rotation without changing actual block state.

        :return: List of Positions for the next rotation state.
        :rtype: list[Position]
        """
        next_rotation = (self.rotation_state + 1) % len(self._cells)
        tiles = self._cells[next_rotation]
        return [
            Position(p.row + self.row_offset, p.column + self.col_offset) for p in tiles
        ]

    def rotate(self) -> None:
        """Rotate the block clockwise by advancing to the next rotation state."""
        self._rotation_state = (self._rotation_state + 1) % len(self._cells)

    def move(self, rows: int, columns: int) -> None:
        """Move the block by a given offset.

        :param rows: Number of rows to shift (positive = down).
        :type rows: int
        :param columns: Number of columns to shift (positive = right).
        :type columns: int
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
