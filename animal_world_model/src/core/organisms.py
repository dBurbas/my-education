import random
import copy
from abc import ABC, abstractmethod
from core.base import Position
from typing import TYPE_CHECKING, Optional
from config import STARTER_ENERGY, STARTER_HEALTH, MAX_ENERGY, MAX_HEALTH

from core.commands import (
    Command,
    EatCommand,
    MoveCommand,
    ReproduceCommand,
    SoundCommand,
    RestCommand,
    PhotosynthesisCommand,
)

if TYPE_CHECKING:
    from ecosystem import Ecosystem


# TODO: доработать все docstring
class Organism(ABC):
    "Abstract base class for all organisms"

    # TODO: подумать над названием id аргумента (не будет ли проблемой с встроенкой)
    def __init__(
        self,
        *,
        id: int,
        name: str,
        position: Position,
        energy: int = STARTER_ENERGY,
        health: int = STARTER_HEALTH,
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
        self._size = size
        self._grow_rate = grow_rate
        self._cost_of_living = 1

    @property
    def organism_id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def position(self) -> Position:
        return self._position

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def health(self) -> int:
        return self._health

    @property
    def age(self) -> int:
        return self._age

    @property
    def size(self) -> float:
        return self._size

    @property
    def grow_rate(self) -> float:
        return self._grow_rate

    @property
    def cost_of_living(self) -> int:
        return self._cost_of_living

    def gain_energy(self, amount: int) -> None:
        self._energy = min(self._energy + amount, MAX_ENERGY)

    def lose_energy(self, amount: int) -> None:
        self._energy -= amount
        if self._energy <= 0:
            self.die()

    def move_to(self, pos: Position) -> None:
        self._position = pos

    def apply_metabolism(self) -> None:
        self._energy -= self._cost_of_living * (self._size / 5)
        if self._energy <= 0:
            self.die()

    def grow(self, amount: int) -> None:
        if amount < 0:
            # TODO: выкидывать исключение
            pass
        self._size += amount

    # TODO: подумать над проверкой про отрицательные значения
    def gain_health(self, amount: int) -> None:
        self._health = min(self._health + amount, MAX_HEALTH)

    def lose_health(self, amount: int) -> None:
        self._health -= amount
        if self._health <= 0:
            self.die()

    # TODO: поменять стиль docstring на :param...
    @abstractmethod
    def behave(self, ecosystem: "Ecosystem") -> list["Command"]:
        """Behave abstract method for all organisms
        Args:
            ecosystem (Ecosystem): Ecosystem in which organism behaves.
        Returns:
            list[Command]: Commands to perform"""
        pass

    def get_older(self) -> None:
        self._age += 1
        if self._energy > 50 and self._age <= 25:
            self._size += 0.5 * self._grow_rate
        if self._age > 25:
            self._health -= int(self._age / 25)

    def clone(self, **kwargs) -> "Organism":
        """
        Makes self deepcopy and reset "living" params
        """
        cloned_obj = copy.deepcopy(self)

        for key, value in kwargs.items():
            attribute_name = f"_{key}" if not hasattr(cloned_obj, key) else key
            setattr(cloned_obj, attribute_name, value)

        cloned_obj._age = 0
        cloned_obj._size = self._size * 0.5
        cloned_obj._energy = STARTER_ENERGY
        cloned_obj._health = STARTER_HEALTH

        return cloned_obj

    # TODO: подумать на счет логики размножения (нужен ли партнер)
    def reproduce(self) -> "ReproduceCommand":
        return ReproduceCommand(reproducer=self)

    def is_alive(self) -> bool:
        """Method to check is organism alive"""
        return self._health > 0

    def die(self) -> None:
        self._health = 0


class Animal(Organism):
    def __init__(
        self, *, hunger_rate: float, vision_radius: float, speed: float, **kwargs
    ):
        super().__init__(**kwargs)
        self._hunger_rate = hunger_rate
        self._vision_radius = vision_radius
        self._speed = speed

    @property
    def hunger_rate(self) -> float:
        return self._hunger_rate

    @property
    def vision_radius(self) -> float:
        return self._vision_radius

    @property
    def speed(self) -> float:
        return self._speed

    @abstractmethod
    def make_sound(self) -> "SoundCommand":
        pass

    def behave(self, ecosystem) -> list["Command"]:
        if not self.is_alive():
            return []
        # TODO: добавить старение
        escape_command = self.suspect(ecosystem)
        if escape_command:
            return [escape_command]
        # TODO: перекинуть в config значение энергии для поиска еды и поменять его на меньшее
        if self._energy < 200:
            food_command = self.find_food(ecosystem)
            if food_command:
                return [food_command]
        # TODO: переделать неправильную логику (отдыхает и бродит, нужно разделить)
        return [self.make_sound(), RestCommand(resting=self), self.wander()]

    def find_food(self, ecosystem: "Ecosystem") -> Optional["Command"]:
        neighbors = ecosystem.get_organisms_in_radius(
            self._position, self._vision_radius
        )

        food_list = [
            n for n in neighbors if ecosystem.food_chain.can_eat(eater=self, eaten=n)
        ]

        if not food_list:
            return None

        closest_food = min(
            food_list, key=lambda f: self._position.distance_to(f._position)
        )

        dist = self._position.distance_to(closest_food._position)

        if dist <= 1.0:
            return EatCommand(eater=self, food=closest_food)

        return MoveCommand(
            mover=self, target_position=closest_food._position, is_sprinting=True
        )

    def suspect(self, ecosystem: "Ecosystem") -> Optional["Command"]:
        neighbors = ecosystem.get_organisms_in_radius(
            self._position, self._vision_radius
        )

        predators = [
            n for n in neighbors if ecosystem.food_chain.can_eat(eater=n, eaten=self)
        ]

        if not predators:
            return None

        closest_predator = min(
            predators, key=lambda p: self._position.distance_to(p._position)
        )

        dx = self._position.x - closest_predator._position.x
        dy = self._position.y - closest_predator._position.y

        safe_pos = Position(self._position.x + dx, self._position.y + dy)

        return MoveCommand(mover=self, target_position=safe_pos, is_sprinting=True)

    def wander(self) -> "MoveCommand":
        random_x = self._position.x + random.uniform(-10, 10)
        random_y = self._position.y + random.uniform(-10, 10)
        target = Position(random_x, random_y)

        return MoveCommand(mover=self, target_position=target)

    def rest(self) -> "RestCommand":
        return RestCommand(resting=self)


class Plant(Organism):
    def __init__(self, *, photosynthesis_rate: float, **kwargs):
        super().__init__(**kwargs)
        self._photosynthesis_rate = photosynthesis_rate

    def behave(self, ecosystem) -> list["Command"]:
        return [
            PhotosynthesisCommand(
                plant=self, photosynthesis_rate=self._photosynthesis_rate
            )
        ]


# TODO: подумать над именованием аргументов (повторяются)
class Grass(Plant):
    def __init__(self, *, photosynthesis_rate=1.0, **kwargs):
        super().__init__(photosynthesis_rate=photosynthesis_rate, **kwargs)


class Wolf(Animal):
    def __init__(self, *, hunger_rate=1.5, vision_radius=10, speed=1, **kwargs):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        return SoundCommand(sound_maker=self, sound="Awoooooof")


class Rabbit(Animal):
    def __init__(self, *, hunger_rate=1, vision_radius=5, speed=1, **kwargs):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        return SoundCommand(sound_maker=self, sound="Chump-chum")


class Fox(Animal):
    def __init__(self, *, hunger_rate=1, vision_radius=7, speed=1.1, **kwargs):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        return SoundCommand(sound_maker=self, sound="What does the fox say")
