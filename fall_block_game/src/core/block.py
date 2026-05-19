# from config.config import SHAPES
from core.colors import Colors
from core.position import Position
import pygame


# TODO: typehints
# TODO: docstrings
class Block:
    def __init__(self, id):
        self._id = id
        self._cells = {}
        self._rotation_state = 0
        self._row_offset = 0
        self._col_offset = 0
        self._cell_size = 30
        self.colors = Colors.get_cell_colors()
        self.get_to_start_pos()

    def rotate(self):
        self._rotation_state = (self._rotation_state + 1) % len(self._cells)

    def undo_rotation(self):
        self._rotation_state = (self._rotation_state - 1) % len(self._cells)

    def get_to_start_pos(self):
        self.move(0, 3)

    def draw(self, screen):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(
                tile.column * self._cell_size + 1,
                tile.row * self._cell_size + 1,
                self._cell_size - 1,
                self._cell_size - 1,
            )
            pygame.draw.rect(screen, self.colors[self._id], tile_rect)

    def move(self, rows, columns):
        self._row_offset += rows
        self._col_offset += columns

    def get_cell_positions(self):
        tiles = self._cells[self._rotation_state]
        moved_tiles = []
        for pos in tiles:
            pos = Position(pos.row + self._row_offset, pos.column + self._col_offset)
            moved_tiles.append(pos)
        return moved_tiles


#         self.rotations = [self.shape]
#         self.rotate_state = 0
#         current = self.rotations[0]
#         for _ in range(3):
#             current = [list(row) for row in zip(*current[::-1])]
#             self.rotations.append(current)


#     def rotate(self):
#         """Return a new rotated shape"""
#         rotated = self.rotations[self.rotation_state]
#         self.rotation_state = (self.rotation_state + 1) % 4

#         return rotated
