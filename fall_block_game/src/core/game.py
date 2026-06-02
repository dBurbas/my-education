from src.core.grid import Grid
from src.core.block import Block
from src.core.position import Position
from src.core.block_factory import IBlockFactory
from src.core.score_calculator import IScoreCalculator
from src.core.speed_strategy import ISpeedStrategy
from src.core.game_event_manager import IGameEventManager
from src.core.game_event import GameEvent
# TODO: cooldown before lockdown
# TODO: combo


class Game:
    """
    Represents the main game logic for a FallBlock game.

    Manages the grid, current and next blocks, scoring, level progression,
    and event dispatching. Interacts with various strategies and factories
    via dependency injection.

    :param grid: The game grid.
    :type grid: Grid
    :param block_factory: Factory for creating random blocks.
    :type block_factory: IBlockFactory
    :param score_calculator: Calculator for score, level, and cleared lines.
    :type score_calculator: IScoreCalculator
    :param speed_strategy: Strategy to determine drop interval based on level.
    :type speed_strategy: ISpeedStrategy
    :param event_manager: Manager for emitting and subscribing to game events.
    :type event_manager: IGameEventManager
    """

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
        """Return `True` if the game is over, `False` otherwise."""
        return self._game_over

    @property
    def score(self) -> int:
        """Return the current score."""
        return self._score_calculator.score

    @property
    def level(self) -> int:
        """Return the current level."""
        return self._score_calculator.level

    @property
    def lines_cleared_total(self) -> int:
        """Return the total number of cleared lines."""
        return self._score_calculator.lines_cleared_total

    @property
    def current_block(self) -> Block:
        """Return the currently active block.

        .. warning:: Read-only.
        """
        return self._current_block

    @property
    def next_block(self) -> Block:
        """Return the next block that will appear."""
        return self._next_block

    @property
    def grid(self) -> Grid:
        """Return the game grid."""
        return self._grid

    def subscribe(self, event: GameEvent, callback) -> None:
        """
        Subscribe a callback to a game event.

        :param event: The event to subscribe to.
        :type event: GameEvent
        :param callback: The callback function to invoke when the event occurs.
        :type callback: Callable
        """
        self._event_manager.subscribe(event, callback)

    def unsubscribe(self, event: GameEvent, callback) -> None:
        """
        Unsubscribe a callback from a game event.

        :param event: The event to unsubscribe from.
        :type event: GameEvent
        :param callback: The callback function that was previously subscribed.
        :type callback: Callable
        """
        self._event_manager.unsubscribe(event, callback)

    def get_drop_interval_ms(self) -> int:
        """
        Get the drop interval in milliseconds for the current level.

        :return: Drop interval in milliseconds.
        :rtype: int
        """
        return self._speed_strategy.get_drop_interval_ms(self._score_calculator.level)

    def reset(self) -> None:
        """Reset the game state (grid, score, blocks) to start a new game."""
        self._game_over = False
        self._score_calculator.reset()
        self._grid.reset()
        self._current_block = self._block_factory.get_random_block()
        self._next_block = self._block_factory.get_random_block()
        self._current_block.move_to_spawn(self._grid.cols)

    def is_block_valid(self) -> bool:
        """
        Check if the current block's position is valid (inside grid and not overlapping).

        :return: `True` if the block is in a valid position, `False` otherwise.
        :rtype: bool
        """
        return self._is_positions_valid(self._current_block.get_cell_positions())

    def get_ghost_positions(self) -> list[Position]:
        """
        Compute the ghost positions (where the current block would land if dropped).

        :return: List of cell positions for the ghost block.
        :rtype: List[Position]
        """
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

    def rotate(self, clockwise: bool = True) -> None:
        """
        Rotate the current block, applying wall kicks if necessary.

        If the rotation (with any valid kick) is possible, the block is rotated and moved.
        Otherwise, a WALL_BUMP event is emitted.

        :param clockwise: If `True` rotate clockwise, otherwise counter-clockwise.
        :type clockwise: bool
        """
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

    def move_sideway(self, left: bool = True) -> None:
        """
        Move the current block left or right by one column if possible.

        :param left: If `True` move left, otherwise move right.
        :type left: bool
        """
        move_val: int = 1
        if left:
            move_val = -move_val

        future_pos = self._current_block.get_moved_positions(0, move_val)

        if self._is_positions_valid(future_pos):
            self._current_block.move(0, move_val)
        else:
            self._event_manager.emit(GameEvent.WALL_BUMP)

    def move_down(self) -> None:
        """
        Move the current block down by one row if possible.

        If movement is not possible, the block is locked.
        A soft drop reward is added to the score.
        """
        future_pos = self._current_block.get_moved_positions(1, 0)

        if self._is_positions_valid(future_pos):
            self._current_block.move(1, 0)
            self._score_calculator.add_soft_drop_reward()
        else:
            self.lock_block()

    def hard_drop(self) -> None:
        """
        Instantly drop the current block to the lowest possible position.

        The block is moved to its ghost position, a hard drop reward is added,
        a HARD_DROP event is emitted, and then the block is locked.
        """
        ghost_tiles = self.get_ghost_positions()

        current_tiles = self._current_block.get_cell_positions()
        drop_distance = ghost_tiles[0].row - current_tiles[0].row
        self._current_block.move(drop_distance, 0)
        self._score_calculator.add_hard_drop_reward(drop_distance)
        self._event_manager.emit(GameEvent.HARD_DROP, self.current_block)
        self.lock_block()

    def lock_block(self) -> None:
        """
        Lock the current block into the grid, clear full rows, update score and level,
        spawn the next block, and check for game over.
        """
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

    def _is_positions_valid(self, positions: list[Position]) -> bool:
        """
        Check if all given positions are inside the grid and empty.

        :param positions: List of positions to validate.
        :type positions: List[Position]
        :return: True if all positions are valid, False otherwise.
        :rtype: bool
        """
        for pos in positions:
            if not self._grid.is_inside(
                pos.row, pos.column
            ) or not self._grid.is_cell_empty(pos.row, pos.column):
                return False
        return True
