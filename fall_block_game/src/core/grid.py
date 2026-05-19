import pygame
from core.colors import Colors


class Grid:
    def __init__(self, rows: int = 20, columns: int = 10, cell_size=30):
        if rows < 1:
            raise ValueError("Expected row value > 0 ")
        self._num_rows = rows
        self._num_columns = columns
        self._cell_size = cell_size

        self._grid = [
            [0 for _ in range(self._num_columns)] for _ in range(self._num_rows)
        ]
        self._colors = Colors.get_cell_colors()

    def is_inside(self, row, column):
        if (
            row >= 0
            and row < self._num_rows
            and column >= 0
            and column < self._num_columns
        ):
            return True
        return False

    def is_cell_empty(self, row, column):
        if self._grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self._num_columns):
            if self._grid[row][column] == 0:
                return False
        return True

    def reset(self):
        for row in range(self._num_rows):
            self.clear_row(row)

    def clear_row(self, row):
        for column in range(self._num_columns):
            self._grid[row][column] = 0

    def move_row_down(self, row, num_rows):
        for col in range(self._num_columns):
            self._grid[row + num_rows][col] = self._grid[row][col]
            self._grid[row][col] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self._num_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed

    def print_grid(self):
        for row in range(self._num_rows):
            for col in self._grid[row]:
                print(col, end=" ")
            print()

    def draw(self, screen):
        for row in range(self._num_rows):
            for col in range(self._num_columns):
                cell_val = self._grid[row][col]
                cell_rect = pygame.Rect(
                    col * self._cell_size + 1,
                    row * self._cell_size + 1,
                    self._cell_size - 1,
                    self._cell_size - 1,
                )
                pygame.draw.rect(screen, self._colors[cell_val], cell_rect)
