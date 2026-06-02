from abc import ABC, abstractmethod


class IScoreCalculator(ABC):
    """Interface for a score calculator.

    Provides methods to update score based on game events and track level progression.
    """

    @property
    @abstractmethod
    def level(self) -> int:
        """Current game level.

        :return: Current level (starting from 1)
        :rtype: int
        """
        pass

    @property
    @abstractmethod
    def lines_cleared_total(self) -> int:
        """Total number of cleared lines since last reset.

        :return: Total cleared lines count
        :rtype: int
        """
        pass

    @property
    @abstractmethod
    def score(self) -> int:
        """Current total score.

        :return: Current score value
        :rtype: int
        """
        pass

    @abstractmethod
    def reset(self):
        """Reset score, level, and total cleared lines to initial state.

        :return: None
        """
        pass

    @abstractmethod
    def add_soft_drop_reward(self):
        """Add soft drop reward to the current score.

        :return: None
        """
        pass

    @abstractmethod
    def add_hard_drop_reward(self, drop_distance: int):
        """Add hard drop reward to the current score.

        :param drop_distance: Number of cells the piece fell during hard drop
        :type drop_distance: int

        :return: None
        """
        pass

    @abstractmethod
    def update_score(self, lines_cleared: int) -> bool:
        """Update score and level based on number of cleared lines.

        :param lines_cleared: Number of lines cleared in a single move
        :type lines_cleared: int

        :return: `True` if level increased, `False` otherwise
        :rtype: bool
        """
        pass


class ScoreCalculator:
    """Concrete score calculator implementing IScoreCalculator.

    Handles scoring logic with configurable rewards, level progression, and maximum level.

    :param line_clear_reward: Base points per cleared line (multiplied by level)
    :type line_clear_reward: int
    :param hard_drop_reward: Points per cell dropped during hard drop
    :type hard_drop_reward: int
    :param soft_drop_reward: Points per soft drop move
    :type soft_drop_reward: int
    :param lines_per_level: Number of lines required to advance one level
    :type lines_per_level: int
    :param max_level: Maximum reachable level
    :type max_level: int
    :param start_level: Starting level (default 1)
    :type start_level: int
    :raises ValueError: If lines_per_level is less than 1
    """

    def __init__(
        self,
        line_clear_reward: int,
        hard_drop_reward: int,
        soft_drop_reward: int,
        lines_per_level: int,
        max_level: int,
        start_level: int = 1,
    ):
        if lines_per_level < 1:
            raise ValueError(
                f"Unexpected value of lines per level: {lines_per_level} . Expected: > 0."
            )
        self._line_clear_reward = line_clear_reward
        self._hard_drop_reward = hard_drop_reward
        self._soft_drop_reward = soft_drop_reward
        self._score: int = 0
        self._lines_per_level = lines_per_level
        self._start_level = start_level
        self._max_level: int = max_level
        self._level: int = start_level
        self._lines_cleared_total: int = 0

    @property
    def level(self) -> int:
        """Current game level.

        :return: Current level (starting from 1)
        :rtype: int
        """
        return self._level

    @property
    def lines_cleared_total(self) -> int:
        """Total number of cleared lines since last reset.

        :return: Total cleared lines count
        :rtype: int
        """
        return self._lines_cleared_total

    @property
    def score(self) -> int:
        """Current total score.

        :return: Current score value
        :rtype: int
        """
        return self._score

    def reset(self):
        """Reset score, level, and total cleared lines to initial state.

        :return: None
        """
        self._score = 0
        self._level = self._start_level
        self._lines_cleared_total = 0

    def add_soft_drop_reward(self):
        """Add soft drop reward to the current score.

        :return: None
        """
        self._score += self._soft_drop_reward

    def add_hard_drop_reward(self, drop_distance: int):
        """Add hard drop reward based on drop distance.

        Reward = drop_distance * hard_drop_reward.

        :param drop_distance: Number of cells the piece fell during hard drop
        :type drop_distance: int
        :return: None
        """
        self._score += drop_distance * self._hard_drop_reward

    def update_score(self, lines_cleared: int) -> int | None:
        """Update score and level based on number of cleared lines.

        Score increment = lines_cleared * line_clear_reward * current_level.
        Total cleared lines increased. Level may increase if lines_per_level threshold crossed,
        but not beyond max_level.

        :param lines_cleared: Number of lines cleared in a single move
        :type lines_cleared: int
        :return: New level if level increased, otherwise None
        :rtype: int or None
        """
        reward = lines_cleared * self._line_clear_reward
        self._score += reward * self._level

        self._lines_cleared_total += lines_cleared
        new_level = (self._lines_cleared_total // self._lines_per_level) + 1
        if new_level > self._level and self._level < self._max_level:
            self._level = new_level
            return new_level
        return None
