from abc import ABC, abstractmethod
from typing import Callable
from src.core.exception import EventError
from src.core.game_event import GameEvent


class IGameEventManager(ABC):
    """Interface for a game event manager.

    Provides methods to subscribe, unsubscribe, and emit game events.
    """

    @abstractmethod
    def subscribe(self, event: GameEvent, callback_function: Callable):
        """Subscribe a callback to a specific game event.

        :param event: The game event to subscribe to.
        :type event: GameEvent
        :param callback_function: Callable to be invoked when the event is emitted.
        :type callback_function: Callable
        :return: None
        """
        pass

    @abstractmethod
    def unsubscribe(self, event: GameEvent, callback_function: Callable):
        """Unsubscribe a callback from a specific game event.

        :param event: The game event to unsubscribe from.
        :type event: GameEvent
        :param callback_function: Callable that was previously subscribed.
        :type callback_function: Callable
        :return: None
        """
        pass

    @abstractmethod
    def emit(self, event: GameEvent, *args, **kwargs):
        """Emit a game event, triggering all subscribed callbacks.

        :param event: The game event to emit.
        :type event: GameEvent
        :param args: Additional positional arguments to pass to callbacks.
        :param kwargs: Additional keyword arguments to pass to callbacks.
        :return: None
        """
        pass


class GameEventManager:
    """Concrete implementation of a game event manager.

    Manages callbacks for each game event type.
    """

    def __init__(self):
        """Initialize the event manager with empty callback lists for all events."""
        self._callbacks = {event: [] for event in GameEvent}

    def subscribe(self, event: GameEvent, callback_function: Callable):
        """Subscribe a callback to a specific game event.

        :param event: The game event to subscribe to.
        :type event: GameEvent
        :param callback_function: Callable to be invoked when the event is emitted.
        :type callback_function: Callable
        :raises EventError: If event is not a GameEvent instance.
        :raises TypeError: If callback_function is not callable.
        :return: None
        """
        if not isinstance(event, GameEvent):
            raise EventError(f"Expected GameEvent, got: {type(event)}")
        if not callable(callback_function):
            raise TypeError(f"Callback must be callable, got {type(callback_function)}")
        self._callbacks[event].append(callback_function)

    @abstractmethod
    def unsubscribe(self, event: GameEvent, callback_function: Callable):
        """Unsubscribe a callback from a specific game event.

        If the callback is not found in the list, the method does nothing.

        :param event: The game event to unsubscribe from.
        :type event: GameEvent
        :param callback_function: Callable that was previously subscribed.
        :type callback_function: Callable
        :raises EventError: If event is not a GameEvent instance.
        :return: None
        """
        if event in self._callbacks:
            try:
                self._callbacks[event].remove(callback_function)
            except ValueError:
                pass
        else:
            raise EventError(f"Expected GameEvent, got: {type(event)}")

    def emit(self, event: GameEvent, *args, **kwargs):
        """Emit a game event, triggering all subscribed callbacks.

        :param event: The game event to emit.
        :type event: GameEvent
        :param args: Additional positional arguments to pass to callbacks.
        :param kwargs: Additional keyword arguments to pass to callbacks.
        :raises EventError: If event is not a GameEvent instance.
        :return: None
        """
        if not isinstance(event, GameEvent):
            raise EventError(f"Expected GameEvent, got: {type(event)}")
        for callback in self._callbacks[event]:
            callback(*args, **kwargs)
