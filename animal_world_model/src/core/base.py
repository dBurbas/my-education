from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Type


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
    def execute():
        pass


# TODO: доработать классы комманд


class EatCommand(Command):
    """Eat command class"""

    def execute(self):
        pass


class MoveCommand(Command):
    """Move command class"""

    def execute(self):
        pass


class DieCommand(Command):
    """Die command class"""

    def execute(self):
        pass


class RestCommand(Command):
    """Rest command class"""

    def execute(self):
        pass


class Organism(ABC):
    "Abstract base class for all organisms"

    def __init__(self, *, id, name, position, energy=100, health=100, age=0, size=1):
        self._id = id
        self._name = name
        self._position = position
        self._energy = energy
        self._health = health
        self._age = age
        self._size = size

    @abstractmethod
    def behave(self) -> list["Command"]:
        """Behave abstract method for all organisms
        Args:
            ecosystem (Ecosystem): Ecosystem in which organism behaves.
        Returns:
            list[Command]: Commands to perform"""
        pass

    def is_alive(self) -> bool:
        return self._health > 0

    def grow(self) -> None:
        self._age += 1
        if self._energy > 50:
            self._size += 0.5
        if self._age >= 25:
            self._health -= 1

    def die(self) -> None:
        self._health = 0


class Animal(Organism):
    def __init__(
        self,
        *,
        id,
        name,
        position,
        hunger_rate: float,
        vision_radius: float,
        speed: int,
        energy=100,
        health=100,
        age=0,
        size=1,
    ):
        super().__init__(id, name, position, energy, health, age, size)
        self._hunger_rate = hunger_rate
        self._vision_radius = vision_radius
        self._speed = speed
        pass

    @abstractmethod
    def make_sound() -> str:
        pass

    # TODO: подумать на счет возвращения Command
    def move() -> None:
        pass

    def find_food() -> None:
        pass

    def escape() -> bool:
        pass

    def hide() -> bool:
        pass

    def eat() -> None:
        pass

    def rest() -> None:
        pass


class Plant(Organism):
    def __init__(self, photosynthesis_rate: float):
        super().__init__()
        self._


class FoodChain:
    diet_rules: dict[Type[Organism], list[Type[Organism]]]

    def can_eat(eater: Organism, eaten: Organism) -> bool:
        pass


class Habitat:
    map_size: tuple[float, float]
    hide_rate: float

    def get_hiding_bonus(animal_to_hide: Animal) -> float:
        pass


class Ecosystem:
    # organism_factory: OrganismFactory
    habitat: Habitat
    organisms: list[Organism]
    food_chain: FoodChain

    def tick():
        pass


class ICorpseDecomposer(ABC):
    @abstractmethod
    def decompose(organisms: list[Organism]) -> list[Organism]:
        pass


class SimpleCorpseDecomposer(ICorpseDecomposer):
    def decompose(organisms: list[Organism]) -> list[Organism]:
        pass
