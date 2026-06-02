from src.core.grid import Grid
from src.core.block import Block
from src.core.position import Position
from src.core.block_factory import IBlockFactory
from src.core.score_calculator import IScoreCalculator
from src.core.speed_strategy import ISpeedStrategy
from src.core.game_event_manager import IGameEventManager
from src.core.game_event import GameEvent
# TODO: сделать кулдаун
# TODO: комбо


# TODO: docstrings
# TODO: typehints


class Game:
    def __init__(
        self,
        grid: Grid,
        block_factory: IBlockFactory,
        score_calculator: IScoreCalculator,
        speed_strategy: ISpeedStrategy,
        event_manager: IGameEventManager,
    ):
        self._grid = grid
        self._block_factory = block_factory
        self._score_calculator = score_calculator
        self._speed_strategy = speed_strategy
        self._event_manager = event_manager

        self._current_block: Block = self._block_factory.get_random_block()
        self._next_block: Block = self._block_factory.get_random_block()
        self._current_block.move_to_spawn(self._grid.cols)

        self._game_over: bool = False

    @property
    def game_over(self) -> bool:
        return self._game_over

    @property
    def score(self) -> int:
        return self._score_calculator.score

    @property
    def level(self) -> int:
        return self._score_calculator.level

    @property
    def lines_cleared_total(self) -> int:
        return self._score_calculator.lines_cleared_total

    @property
    def current_block(self) -> Block:
        return self._current_block

    @property
    def next_block(self) -> Block:
        return self._next_block

    @property
    def grid(self) -> Grid:
        return self._grid

    def subscribe(self, event: GameEvent, callback):
        self._event_manager.subscribe(event, callback)

    def unsubscribe(self, event: GameEvent, callback):
        self._event_manager.unsubscribe(event, callback)

    def get_drop_interval_ms(self):
        return self._speed_strategy.get_drop_interval_ms(self._score_calculator.level)

    def reset(self):
        self._game_over = False
        self._score_calculator.reset()
        self._grid.reset()
        self._current_block = self._block_factory.get_random_block()
        self._next_block = self._block_factory.get_random_block()
        self._current_block.move_to_spawn(self._grid.cols)

    def is_block_valid(self):
        return self._is_positions_valid(self._current_block.get_cell_positions())

    def get_ghost_positions(self) -> list:
        current_tiles = self._current_block.get_cell_positions()
        drop_distance = 0

        while True:
            future_tiles = [
                Position(p.row + drop_distance + 1, p.column) for p in current_tiles
            ]
            if self._is_positions_valid(future_tiles):
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
        kicks = self._current_block.get_kick_translations(clockwise)

        for dx, dy in kicks:
            future_pos = self._current_block.get_rotated_and_moved_positions(
                d_row=dy, d_col=dx, clockwise=clockwise
            )

            if self._is_positions_valid(future_pos):
                self._current_block.rotate(clockwise)
                self._current_block.move(dy, dx)
                return

        self._event_manager.emit(GameEvent.WALL_BUMP)

    def move_sideway(self, left: bool = True):
        move_val: int = 1
        if left:
            move_val = -move_val

        future_pos = self._current_block.get_moved_positions(0, move_val)

        if self._is_positions_valid(future_pos):
            self._current_block.move(0, move_val)
        else:
            self._event_manager.emit(GameEvent.WALL_BUMP)

    def move_down(self):
        future_pos = self._current_block.get_moved_positions(1, 0)

        if self._is_positions_valid(future_pos):
            self._current_block.move(1, 0)
            self._score_calculator.add_soft_drop_reward()
        else:
            self.lock_block()

    def hard_drop(self):
        ghost_tiles = self.get_ghost_positions()

        current_tiles = self._current_block.get_cell_positions()
        drop_distance = ghost_tiles[0].row - current_tiles[0].row
        self._current_block.move(drop_distance, 0)
        self._score_calculator.add_hard_drop_reward(drop_distance)
        self._event_manager.emit(GameEvent.HARD_DROP, self.current_block)
        self.lock_block()

    def lock_block(self):
        tiles = self._current_block.get_cell_positions()
        for pos in tiles:
            self._grid.set_cell(pos.row, pos.column, self._current_block.id)

        self._event_manager.emit(GameEvent.LOCK)

        lines_cleared, lines_idx = self._grid.clear_full_rows()

        if lines_cleared > 0:
            self._event_manager.emit(GameEvent.LINES_CLEARED, lines_idx)
            new_level = self._score_calculator.update_score(lines_cleared)
            if new_level is not None:
                new_timer_ms = self._speed_strategy.get_drop_interval_ms(new_level)
                self._event_manager.emit(GameEvent.LEVEL_UP, new_level, new_timer_ms)

        self._current_block = self._next_block
        self._next_block = self._block_factory.get_random_block()
        self._current_block.move_to_spawn(self._grid.cols)

        if not self.is_block_valid():
            self._game_over = True
            self._event_manager.emit(GameEvent.GAME_OVER)

    def _is_positions_valid(self, positions: list[Position]):
        for pos in positions:
            if not self._grid.is_inside(
                pos.row, pos.column
            ) or not self._grid.is_cell_empty(pos.row, pos.column):
                return False
        return True
