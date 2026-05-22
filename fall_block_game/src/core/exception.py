class FallBlockError(Exception):
    """Base exception for the project"""

    pass


class GridError(FallBlockError):
    """Exception for wrong grid values"""

    pass


class GridCellError(GridError):
    """Exception for wrong grid cell values"""

    def __init__(
        self,
        row_value: int,
        col_value: int,
        value: int,
        max_row: int,
        max_col: int,
    ):
        self.row_value = row_value
        self.col_value = col_value
        self.cell_value = value
        self.max_row = max_row
        self.max_col = max_col
        super().__init__(
            f"Grid cell values are incorrect cords: ({row_value},{col_value}), value:{value}.\
                Expected positive int values like cords: (1, 1), value: 0. Max cords: ({max_row},{max_col})"
        )


class BlockFactoryError(FallBlockError):
    """Exception for block factory errors"""

    pass


class EventError(FallBlockError):
    """Exception for event errors"""

    pass
