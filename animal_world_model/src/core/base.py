from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Type
from enums import EventType


# TODO: доработать все docstring
@dataclass
class Position:
    """Position class for entities positions"""

    x: float
    y: float

    def distance_to(self, other: "Position") -> float:
        """Calculate the distance to another position using the Euclidean distance formula.
        Args:
            other (Position): The other position to which the distance is calculated.
        Returns:
            float: The distance to the other position."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Command(ABC):
    """Abstract base class for all comands"""

    @abstractmethod
    def execute(self, ecosystem: "Ecosystem") -> None:
        pass


class EatCommand(Command):
    """Eat command class"""

    def __init__(self, *, eater: "Organism", food: "Organism"):
        self._eater = eater
        self._food = food

    def execute(self, ecosystem: "Ecosystem") -> None:
        self._food.die()
        self._eater._energy += self._food._energy
        # TODO: подумать над перееданием, увеличивать максимальную энергию
        if self._eater._energy > 100:
            self._eater._energy = 100

        ecosystem.event_manager.publish(
            EventType.DIE_EVENT,
            {"dead": self._food._name, "cause": EventType.EAT_EVENT},
        )
        ecosystem.event_manager.publish(
            EventType.EAT_EVENT, {"eater": self._eater._name, "food": self._food._name}
        )


class PhotosynthesisCommand(Command):
    """Photosynthesis command class"""

    def __init__(self, *, plant: "Plant", photosynthesis_rate: float):
        self._photosynthesis_rate = photosynthesis_rate
        self._plant = plant

    def execute(self, ecosystem: "Ecosystem") -> None:
        increase = 0.5 * self._photosynthesis_rate
        self._plant._size += increase
        self._plant._energy += increase * 10
        ecosystem.event_manager.publish(
            EventType.PHOTOSYNTHESIS_EVENT,
            {"plant": self._plant, "increase": increase},
        )


class MoveCommand(Command):
    """Move command class"""

    # TODO: MoveCommand
    def execute(self, ecosystem: "Ecosystem") -> None:
        pass


class RestCommand(Command):
    """Rest command class"""

    # TODO: RestCommand
    def execute(self, ecosystem: "Ecosystem") -> None:
        pass


class ReproduceCommand(Command):
    """Reproduce command class"""

    def __init__(self, *, reproducer: "Organism"):
        self._reproducer = reproducer

    def execute(self, ecosystem: "Ecosystem") -> None:
        pass


class SexualReproductionCommand(ReproduceCommand):
    """Reproduction command class for sexual reproduction(2 parents)"""

    def __init__(self, *, reproducer1: "Organism", reproducer2: "Organism"):
        self._reproducer1 = reproducer1
        self._reproducer2 = reproducer2

    def execute(self, ecosystem: "Ecosystem") -> None:
        pass


class SoundCommand(Command):
    """Sound command class"""

    def __init__(self, *, sound_maker: "Organism", sound: str):
        self._sound_maker = sound_maker
        self._sound = sound

    def execute(self, ecosystem: "Ecosystem") -> None:
        ecosystem.event_manager.publish(
            EventType.SOUND_EVENT,
            {"sound_maker": self._sound_maker, "sound": self._sound},
        )


# TODO: WanderCommand
class Organism(ABC):
    "Abstract base class for all organisms"

    def __init__(
        self,
        *,
        id: int,
        name: str,
        position: Position,
        energy: int = 100,
        health: int = 100,
        age: int = 0,
        size: float = 1.0,
        grow_rate: float = 1.0,
    ):
        self._id = id
        self._name = name
        self._position = position
        self._energy = energy
        self._health = health
        self._age = age
        # TODO: подумать на счет optional size_limit поля
        self._size = size
        self._grow_rate = grow_rate

    @abstractmethod
    def behave(self, ecosystem: "Ecosystem") -> list["Command"]:
        """Behave abstract method for all organisms
        Args:
            ecosystem (Ecosystem): Ecosystem in which organism behaves.
        Returns:
            list[Command]: Commands to perform"""
        pass

    def is_alive(self) -> bool:
        return self._health > 0

    # TODO: подумать над логикой роста, может животному тоже сделать
    def grow(self) -> None:
        self._age += 1
        if self._energy > 50 and self._age <= 25:
            self._size += 0.5 * self._grow_rate
        if self._age > 25:
            self._health -= 1

    # TODO: может сделать звук после размножения
    def reproduce(self) -> "ReproduceCommand":
        return ReproduceCommand(reproducer=self)

    def die(self) -> None:
        self._health = 0.0


class Animal(Organism):
    def __init__(
        self, *, hunger_rate: float, vision_radius: float, speed: float, **kwargs
    ):
        super().__init__(**kwargs)
        self._hunger_rate = hunger_rate
        self._vision_radius = vision_radius
        self._speed = speed

    @abstractmethod
    def make_sound(self) -> SoundCommand:
        pass

    # TODO: подумать на счет возвращения Command
    def move(self) -> MoveCommand:
        pass

    def find_food() -> None:
        pass

    def escape() -> bool:
        pass

    def hide() -> bool:
        pass

    def eat() -> EatCommand:
        pass

    def rest() -> RestCommand:
        pass


class Plant(Organism):
    def __init__(self, *, photosynthesis_rate: float, **kwargs):
        super().__init__(**kwargs)
        self._photosynthesis_rate = photosynthesis_rate


class FoodChain:
    diet_rules: dict[Type[Organism], list[Type[Organism]]]

    def can_eat(eater: Organism, eaten: Organism) -> bool:
        pass


class Habitat:
    # TODO: проверить класс
    map_size: tuple[float, float] = (10.0, 10.0)
    hide_rate: float
    success_hide_rate: float

    def get_hiding_bonus(self, animal_to_hide: Animal) -> float:
        pass

    def is_in_bounds(self, position: Position) -> bool:
        return (position.x > 0.0 and position.x < self.map_size[1]) and (
            position.y > 0.0 and position.y < self.map_size[2]
        )


class EventManager:
    pass


# TODO: сделать логику tick()
class Ecosystem:
    # organism_factory: OrganismFactory

    def __init__(
        self,
        *,
        some_event_manager: "EventManager",
        some_habitat: "Habitat",
        some_organisms: list["Organism"],
        some_food_chain: "FoodChain",
    ):
        self.event_manager = some_event_manager
        self.habitat = some_habitat
        self.organisms = some_organisms
        self.food_chain = some_food_chain

    def tick():
        pass
