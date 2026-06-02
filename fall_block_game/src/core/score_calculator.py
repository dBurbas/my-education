from abc import ABC, abstractmethod


class IScoreCalculator(ABC):
    @property
    @abstractmethod
    def level(self) -> int:
        pass

    @property
    @abstractmethod
    def lines_cleared_total(self) -> int:
        pass

    @property
    @abstractmethod
    def score(self) -> int:
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def add_soft_drop_reward(self):
        pass

    @abstractmethod
    def add_hard_drop_reward(self):
        pass

    @abstractmethod
    def update_score(self, lines_cleared: int) -> bool:
        pass


class ScoreCalculator:
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
        return self._level

    @property
    def lines_cleared_total(self) -> int:
        return self._lines_cleared_total

    @property
    def score(self) -> int:
        return self._score

    def reset(self):
        self._score = 0
        self._level = self._start_level
        self._lines_cleared_total = 0

    def add_soft_drop_reward(self):
        self._score += self._soft_drop_reward

    def add_hard_drop_reward(self, drop_distance: int):
        self._score += drop_distance * self._hard_drop_reward

    def update_score(self, lines_cleared: int) -> int | None:
        reward = lines_cleared * self._line_clear_reward
        self._score += reward * self._level

        self._lines_cleared_total += lines_cleared
        new_level = (self._lines_cleared_total // self._lines_per_level) + 1
        if new_level > self._level and self._level < self._max_level:
            self._level = new_level
            return new_level
        return None
