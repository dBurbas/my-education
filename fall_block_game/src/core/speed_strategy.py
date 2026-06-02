from abc import ABC, abstractmethod


class ISpeedStrategy(ABC):
    """Abstract base class defining the interface for drop interval calculation strategies."""

    @abstractmethod
    def get_drop_interval_ms(self, level: int) -> int:
        """Calculate the drop interval in milliseconds for a given level.

        :param level: The current game level (1-based index).
        :type level: int
        :return: The time interval in milliseconds between drops.
        :rtype: int
        """
        pass


class SpeedStrategy(ISpeedStrategy):
    """
    Concrete implementation of ISpeedStrategy that calculates drop intervals
    using a base time, a linear reduction factor, and an exponential modifier.

    :param base_time: The base drop interval in seconds for level 1. Defaults to 0.8.
    :type base_time: float
    :param reduction: The amount by which the base time is reduced per level. Defaults to 0.005.
    :type reduction: float
    :param min_ms: The minimum allowed drop interval in milliseconds. Defaults to 0.
    :type min_ms: int
    """

    def __init__(
        self, base_time: float = 0.8, reduction: float = 0.005, min_ms: int = 0
    ):
        self._base_time: float = base_time
        self._reduction: float = reduction
        self._min_ms: int = min_ms

    def get_drop_interval_ms(self, level: int) -> int:
        """Calculate the drop interval in milliseconds for the given level.

        The calculation applies a exponential reduction to the base time, enforces a
        minimum of 0.1 seconds before raising the result to the power of (level - 1),
        converts the value to milliseconds, and applies the minimum millisecond constraint.

        :param level: The current game level (1-based index).
        :type level: int
        :return: The calculated drop interval in milliseconds.
        :rtype: int
        """
        time_sec = (max(self._base_time - ((level - 1) * self._reduction), 0.1)) ** (
            level - 1
        )

        calculated_ms = int(time_sec * 1000)

        return max(calculated_ms, self._min_ms)
