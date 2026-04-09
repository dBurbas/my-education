from typing import Callable
from core.enums import EventType


class EventManager:
    """Pub/Sub event dispatcher for the simulation.

    Maintains a registry of listeners keyed by :class:`EventType`.
    All event types are pre-registered on construction.
    """

    def __init__(self):
        """The EventManager constructor with empty listener lists for every EventType."""
        self._listeners: dict[EventType, list[Callable]] = {
            event_type: [] for event_type in EventType
        }

    def subscribe(
        self, event_type: EventType, listener: Callable[[dict], None]
    ) -> None:
        """Register a listener callback for a given event type.

        :param event_type: The event type to listen for.
        :type event_type: EventType
        :param listener: Callable that accepts an event data dict.
        :type listener: Callable[[dict], None]
        """
        self._listeners[event_type].append(listener)

    def unsubscribe(
        self, event_type: EventType, listener: Callable[[dict], None]
    ) -> None:
        """Remove a previously registered listener for a given event type.

        Does nothing if the listener is not currently subscribed.

        :param event_type: The event type to stop listening for.
        :type event_type: EventType
        :param listener: The callable to remove.
        :type listener: Callable[[dict], None]
        """
        if listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)

    def publish(self, event_type: EventType, data: dict) -> None:
        """Send all listeners an event registered for its type.

        :param event_type: The type of event being published.
        :type event_type: EventType
        :param data: Payload dict passed to every listener.
        :type data: dict
        """
        for listener in self._listeners[event_type]:
            listener(data)
