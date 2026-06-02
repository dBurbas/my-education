from abc import ABC, abstractmethod
from typing import Callable
from src.core.exception import EventError
from src.core.game_event import GameEvent


class IGameEventManager(ABC):
    @abstractmethod
    def subscribe(self, event: GameEvent, callback_function: Callable):
        pass

    @abstractmethod
    def unsubscribe(self, event: GameEvent, callback_function: Callable):
        pass

    @abstractmethod
    def emit(self, event: GameEvent, *args, **kwargs):
        pass


class GameEventManager:
    def __init__(self):
        self._callbacks = {event: [] for event in GameEvent}

    def subscribe(self, event: GameEvent, callback_function: Callable):
        if not isinstance(event, GameEvent):
            raise EventError(f"Expected GameEvent, got: {type(event)}")
        if not callable(callback_function):
            raise TypeError(f"Callback must be callable, got {type(callback_function)}")
        self._callbacks[event].append(callback_function)

    @abstractmethod
    def unsubscribe(self, event: GameEvent, callback_function: Callable):
        if event in self._callbacks:
            try:
                self._callbacks[event].remove(callback_function)
            except ValueError:
                pass

    def emit(self, event: GameEvent, *args, **kwargs):
        if not isinstance(event, GameEvent):
            raise EventError(f"Expected GameEvent, got: {type(event)}")
        for callback in self._callbacks[event]:
            callback(*args, **kwargs)
