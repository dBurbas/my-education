from abc import ABC, abstractmethod


class ISpeedStrategy(ABC):
    @abstractmethod
    def get_drop_interval_ms(self, level: int) -> int:
        pass


class SpeedStrategy(ISpeedStrategy):
    def __init__(
        self, base_time: float = 0.8, reduction: float = 0.005, min_ms: int = 0
    ):
        self._base_time = base_time
        self._reduction = reduction
        self._min_ms = min_ms

    def get_drop_interval_ms(self, level: int) -> int:
        time_sec = (max(self._base_time - ((level - 1) * self._reduction), 0.1)) ** (
            level - 1
        )

        calculated_ms = int(time_sec * 1000)

        return max(calculated_ms, self._min_ms)
