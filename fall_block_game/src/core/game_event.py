from enum import Enum


class GameEvent(Enum):
    LOCK = "on_lock"
    HARD_DROP = "on_hard_drop"
    WALL_BUMP = "on_wall_bump"
    GAME_OVER = "on_game_over"
    LINES_CLEARED = "on_lines_cleared"
    LEVEL_UP = "on_level_up"
