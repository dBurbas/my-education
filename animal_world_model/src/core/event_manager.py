from typing import Callable
from core.enums import EventType


class EventManager:
    def __init__(self):
        self._listeners: dict[EventType, list[Callable]] = {
            event_type: [] for event_type in EventType
        }

    def subscribe(
        self, event_type: EventType, listener: Callable[[dict], None]
    ) -> None:
        """Adds a listener for a specific type of event."""
        self._listeners[event_type].append(listener)

    def unsubscribe(
        self, event_type: EventType, listener: Callable[[dict], None]
    ) -> None:
        """Removes a listener."""
        if listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)

    def publish(self, event_type: EventType, data: dict) -> None:
        """Notifies all listeners about the occurring event."""
        for listener in self._listeners[event_type]:
            listener(data)
