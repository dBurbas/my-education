from abc import ABC, abstractmethod
from typing import Type, TYPE_CHECKING
from core.base import Position
from core.enums import EventType
from typing import Callable

if TYPE_CHECKING:
    from commands import Command
    from organisms import Organism


# TODO: доработать все docstring
class FoodChain:
    def __init__(self, *, diet_rules: dict[Type["Organism"], list[Type["Organism"]]]):
        self._diet_rules = diet_rules

    def can_eat(self, *, eater: "Organism", eaten: "Organism") -> bool:
        if type(eater) in self._diet_rules:
            return type(eaten) in self._diet_rules[type(eater)]

    def add_rule(
        self, *, eater_type: Type["Organism"], eaten_type: Type["Organism"]
    ) -> None:
        if eater_type in self._diet_rules:
            if eaten_type not in self._diet_rules[eater_type]:
                self._diet_rules[eater_type].append(eaten_type)
        else:
            self._diet_rules[eater_type] = [eaten_type]

    def remove_rule(
        self, *, eater_type: Type["Organism"], eaten_type: Type["Organism"]
    ) -> None:
        if (
            eater_type in self._diet_rules
            and eaten_type in self._diet_rules[eater_type]
        ):
            self._diet_rules[eater_type].remove(eaten_type)


class Habitat:
    def __init__(self, map: tuple[float, float] = (10.0, 10.0)):
        self._map = map

    def clamp_position(self, pos: Position) -> Position:
        """Clamps the position within the map boundaries"""
        max_x, max_y = self._map

        clamped_x = max(0.0, min(pos.x, max_x))
        clamped_y = max(0.0, min(pos.y, max_y))

        return Position(clamped_x, clamped_y)


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


class OrganismFactory(ABC):
    @abstractmethod
    def create_offspring(self, parent: "Organism") -> "Organism":
        pass


class DefaultOrganismFactory(OrganismFactory):
    def __init__(self):
        self._next_id = 1

    def _get_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def create_offspring(self, parent: "Organism") -> "Organism":
        new_pos = Position(parent._position.x + 1, parent._position.y + 1)
        baby_id = self._get_id()
        baby = parent.clone(
            id=baby_id, name=f"{parent._name} Jr. {baby_id}", position=new_pos
        )

        return baby


class Ecosystem:
    def __init__(
        self,
        *,
        some_event_manager: "EventManager",
        some_habitat: "Habitat",
        some_organisms: list["Organism"],
        some_food_chain: "FoodChain",
        factory: OrganismFactory,
    ):
        self.event_manager = some_event_manager
        self.habitat = some_habitat
        self.organisms = some_organisms
        self.food_chain = some_food_chain
        self.factory = factory

    def tick(self):
        self.organisms = [org for org in self.organisms if org.is_alive()]
        all_commands: list["Command"] = []
        for organism in self.organisms:
            if organism.is_alive():
                organism.apply_metabolism()
            if organism.is_alive():
                behavior: list["Command"] = organism.behave(self)
                all_commands.extend(behavior)

        for command in all_commands:
            command.execute(self)

        for organism in self.organisms:
            if organism.is_alive():
                organism.grow()

    def get_organisms_in_radius(
        self, center_pos: "Position", radius: float
    ) -> list["Organism"]:
        "Returns all living organisms within a given radius."
        neighbors = []

        for org in self.organisms:
            if not org.is_alive():
                continue

            dist = center_pos.distance_to(org._position)

            if dist <= radius and dist > 0.0001:
                neighbors.append(org)

        return neighbors
