"""Tests for EventManager"""

import pytest
from core.event_manager import EventManager
from core.enums import EventType


class TestEventManager:
    def test_subscribe_and_publish(self):
        em = EventManager()
        received = []
        em.subscribe(EventType.EAT_EVENT, lambda d: received.append(d))
        em.publish(EventType.EAT_EVENT, {"eater": "Wolf"})
        assert received == [{"eater": "Wolf"}]

    def test_multiple_listeners_same_event(self):
        em = EventManager()
        log1, log2 = [], []
        em.subscribe(EventType.DIE_EVENT, lambda d: log1.append(d))
        em.subscribe(EventType.DIE_EVENT, lambda d: log2.append(d))
        em.publish(EventType.DIE_EVENT, {"dead": "Rabbit"})
        assert len(log1) == 1
        assert len(log2) == 1

    def test_unsubscribe_stops_receiving(self):
        em = EventManager()
        received = []
        handler = lambda d: received.append(d)
        em.subscribe(EventType.MOVE_EVENT, handler)
        em.unsubscribe(EventType.MOVE_EVENT, handler)
        em.publish(EventType.MOVE_EVENT, {"mover": "Wolf"})
        assert received == []

    def test_publish_no_listeners_does_not_raise(self):
        em = EventManager()
        em.publish(EventType.SOUND_EVENT, {"sound": "test"})

    def test_all_event_types_registered_on_init(self):
        em = EventManager()
        for event_type in EventType:
            assert event_type in em._listeners

    def test_listeners_are_isolated_per_event(self):
        em = EventManager()
        eat_log = []
        em.subscribe(EventType.EAT_EVENT, lambda d: eat_log.append(d))
        em.publish(EventType.DIE_EVENT, {"dead": "Fox"})
        assert eat_log == []

    def test_listeners_lists_are_independent_objects(self):
        em = EventManager()
        em._listeners[EventType.EAT_EVENT].append("x")
        assert "x" not in em._listeners[EventType.DIE_EVENT]
