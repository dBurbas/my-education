from src.core.grid import Grid
from src.core.block import Block
from src.core.block_factory import IBlockFactory
from src.core.position import Position
from src.core.game_config import LogicConfig
from src.core.exception import EventError


# TODO: docstrings
# TODO: typehints
# TODO: wallkicks
class Game:
    def __init__(self, grid: Grid, block_factory: IBlockFactory, config: LogicConfig):
        self._grid = grid
        self._block_factory = block_factory

        self._score_rewards = config.score_rewards
        self._lines_per_level = config.lines_per_level
        self._max_level = config.max_level

        self._current_block: Block = self._block_factory.get_random_block()
        self._next_block: Block = self._block_factory.get_random_block()
        self._game_over: bool = False

        self._score: int = 0
        self._level: int = 1
        self._lines_cleared_total: int = 0
        self._speed_settings = config.speed_curve

        self._current_block.move_to_spawn(self._grid.cols)

        self._callbacks = {
            "on_lock": [],
            "on_hard_drop": [],
            "on_wall_bump": [],
            "on_game_over": [],
            "on_lines_cleared": [],
            "on_level_up": [],
        }

    @property
    def level(self) -> int:
        return self._level

    @property
    def lines_cleared_total(self) -> int:
        return self._lines_cleared_total

    @property
    def score(self) -> int:
        return self._score

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def current_block(self) -> Block:
        return self._current_block

    @property
    def next_block(self) -> Block:
        return self._next_block

    @property
    def grid(self) -> Grid:
        return self._grid

    def subscribe(self, event_name: str, callback_function):
        if event_name in self._callbacks:
            self._callbacks[event_name].append(callback_function)
        else:
            raise EventError(f"Unknown event: {event_name}")

    def _emit(self, event_name: str, *args, **kwargs):
        for callback in self._callbacks[event_name]:
            callback(*args, **kwargs)

    def reset(self):
        self._game_over = False
        self._score = 0
        self._level = 1
        self._lines_cleared_total = 0
        self._grid.reset()
        self._current_block = self._block_factory.get_random_block()
        self._next_block = self._block_factory.get_random_block()
        self._current_block.move_to_spawn(self._grid.cols)

    def is_block_valid(self):
        return self._are_positions_valid(self._current_block.get_cell_positions())

    def get_ghost_positions(self) -> list:
        current_tiles = self._current_block.get_cell_positions()
        drop_distance = 0

        while True:
            future_tiles = [
                Position(p.row + drop_distance + 1, p.column) for p in current_tiles
            ]

            if self._are_positions_valid(future_tiles):
                drop_distance += 1
            else:
                break

        return [Position(p.row + drop_distance, p.column) for p in current_tiles]

    def rotate(self, clockwise: bool = True):
        # Without wallkick
        # future_pos = self._current_block.get_rotated_positions()
        # print(future_pos)
        # if self._is_positions_valid(future_pos):
        #     self._current_block.rotate()
        kicks = self.current_block.get_kick_translations(clockwise)

        for dx, dy in kicks:
            future_pos = self.current_block.get_rotated_and_moved_positions(
                d_row=dy, d_col=dx, clockwise=clockwise
            )

            if self._is_positions_valid(future_pos):
                self.current_block.rotate(clockwise)
                self.current_block.move(dy, dx)
                return
            # TODO: событие при неудачном повороте(ни один кик не подошел)

    def move_left(self):
        future_pos = self._current_block.get_moved_positions(0, -1)

        if self._are_positions_valid(future_pos):
            self._current_block.move(0, -1)
        else:
            self._emit("on_wall_bump")

    def move_right(self):
        future_pos = self._current_block.get_moved_positions(0, 1)

        if self._are_positions_valid(future_pos):
            self._current_block.move(0, 1)
        else:
            self._emit("on_wall_bump")

    def move_down(self):
        future_pos = self._current_block.get_moved_positions(1, 0)

        if self._are_positions_valid(future_pos):
            self._current_block.move(1, 0)
            self._score += 1 * self._score_rewards.get("soft_drop", 1)
        else:
            self.lock_block()

    def hard_drop(self):
        ghost_tiles = self.get_ghost_positions()

        current_tiles = self._current_block.get_cell_positions()
        drop_distance = ghost_tiles[0].row - current_tiles[0].row
        self._score += drop_distance * self._score_rewards.get("hard_drop", 2)
        self._current_block.move(drop_distance, 0)
        self._emit("on_hard_drop", self.current_block)
        self.lock_block()

    def lock_block(self):
        tiles = self._current_block.get_cell_positions()
        for pos in tiles:
            self._grid.set_cell(pos.row, pos.column, self._current_block.id)

        self._emit("on_lock")

        lines_cleared, lines_idx = self._grid.clear_full_rows()

        if lines_cleared > 0:
            self._emit("on_lines_cleared", lines_idx)
            self._update_score(lines_cleared)

        self._current_block = self._next_block
        self._next_block = self._block_factory.get_random_block()

        self._current_block.move_to_spawn(self._grid.cols)

    def _are_positions_valid(self, positions: list):
        for pos in positions:
            if not self._grid.is_inside(
                pos.row, pos.column
            ) or not self._grid.is_cell_empty(pos.row, pos.column):
                return False
        return True

    def _update_score(self, lines_cleared: int):

        reward = lines_cleared * self._score_rewards.get("line_cleared", 100)
        self._score += reward * self._level

        self._lines_cleared_total += lines_cleared
        new_level = (self._lines_cleared_total // self._lines_per_level) + 1
        if new_level > self._level and self._level < self._max_level:
            self._level = new_level
            new_timer_ms = self.get_drop_interval_ms()
            self._emit("on_level_up", self._level, new_timer_ms)

    def get_drop_interval_ms(self) -> int:
        base_time = self._speed_settings.get("base_time_sec", 0.8)
        reduction = self._speed_settings.get("reduction_per_level", 0.007)
        min_ms = self._speed_settings.get("min_time_ms", 0)

        time_sec = (max(base_time - ((self._level - 1) * reduction), 0.01)) ** (
            self._level - 1
        )

        calculated_ms = int(time_sec * 1000)

        return max(calculated_ms, min_ms)
