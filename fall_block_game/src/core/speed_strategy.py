from abc import ABC, abstractmethod


class ISpeedStrategy(ABC):
    @abstractmethod
    def get_drop_interval_ms(self, level: int) -> int:
        pass


class SpeedStrategy(ISpeedStrategy):
    def __init__(self, speed_settings: dict):
        self._base_time = speed_settings.get("base_time_sec", 0.8)
        self._reduction = speed_settings.get("reduction_per_level", 0.005)
        self._min_ms = speed_settings.get("min_time_ms", 0)

    def get_drop_interval_ms(self, level: int) -> int:
        time_sec = (max(self._base_time - ((level - 1) * self._reduction), 0.1)) ** (
            level - 1
        )

        calculated_ms = int(time_sec * 1000)

        return max(calculated_ms, self._min_ms)
