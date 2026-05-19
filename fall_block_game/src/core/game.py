from core.grid import Grid
from core.block import Block
from core.blocks import IBlock, JBlock, LBlock, OBlock, SBlock, ZBlock, TBlock
import random


class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [
            IBlock(),
            JBlock(),
            LBlock(),
            OBlock(),
            SBlock(),
            ZBlock(),
            TBlock(),
        ]
        self.current_block: Block = self.get_random_block()
        self.next_block: Block = self.get_random_block()
        self.game_over = False

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [
                IBlock(),
                JBlock(),
                LBlock(),
                OBlock(),
                SBlock(),
                ZBlock(),
                TBlock(),
            ]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def reset(self):
        self.grid.reset()
        self.blocks = [
            IBlock(),
            JBlock(),
            LBlock(),
            OBlock(),
            SBlock(),
            ZBlock(),
            TBlock(),
        ]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

    def move_left(self):
        self.current_block.move(0, -1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if not self.block_inside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_cell_empty(tile.row, tile.column):
                return False
        return True

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for pos in tiles:
            self.grid._grid[pos.row][pos.column] = self.current_block._id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        self.grid.clear_full_rows()
        if not self.block_fits():
            self.game_over = True

    def rotate(self):
        self.current_block.rotate()
        if not self.block_inside():
            self.current_block.undo_rotation()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if not self.grid.is_inside(tile.row, tile.column):
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen)
