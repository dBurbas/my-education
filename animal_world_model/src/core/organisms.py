import random
import copy
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional
from config import (
    STARTER_ENERGY,
    STARTER_HEALTH,
    MAX_ENERGY,
    MAX_HEALTH,
    MIN_ENERGY_TO_SEEK_FOOD,
    COMFORT_ENERGY_LEVEL,
    SOUND_PRODUCTION_CHANCE,
    MIN_DISTANCE_TO_EAT,
    DEFAULT_COST_OF_LIVING,
)

from core.base import Position
from core.commands import (
    Command,
    EatCommand,
    MoveCommand,
    ReproduceCommand,
    SoundCommand,
    RestCommand,
    PhotosynthesisCommand,
)
from exception.animal_world_exceptions import (
    GrowthValueError,
    HealthValueError,
    EnergyValueError,
)

if TYPE_CHECKING:
    from ecosystem import Ecosystem


# TODO: доработать все docstring
class Organism(ABC):
    """Abstract base class for all organisms"""

    def __init__(
        self,
        *,
        organism_id: int,
        name: str,
        position: Position,
        energy: int = STARTER_ENERGY,
        health: int = STARTER_HEALTH,
        age: int = 0,
        size: float = 1.0,
        grow_rate: float = 1.0,
    ):
        """Constructor method"""
        self._id = organism_id
        self._name = name
        self._position = position
        self._energy = energy
        self._health = health
        self._age = age
        self._size = size
        self._grow_rate = grow_rate
        self._cost_of_living = DEFAULT_COST_OF_LIVING

    @property
    def organism_id(self) -> int:
        """Property method for id field of organism"""
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
        if amount < 0:
            raise EnergyValueError(amount)
        self._energy = min(self._energy + amount, MAX_ENERGY)

    def lose_energy(self, amount: int) -> None:
        if amount < 0:
            raise EnergyValueError(amount)
        self._energy -= amount
        if self._energy <= 0:
            self.die()

    def move_to(self, pos: Position) -> None:
        self._position = pos

    def apply_metabolism(self) -> None:
        self._energy -= int(self._cost_of_living * (self._size))
        if self._energy <= 0:
            self.die()

    def grow(self, amount: int) -> None:
        if amount < 0:
            raise GrowthValueError(amount)
        self._size += amount

    def gain_health(self, amount: int) -> None:
        if amount < 0:
            raise HealthValueError(amount)
        self._health = min(self._health + amount, MAX_HEALTH)

    def lose_health(self, amount: int) -> None:
        if amount < 0:
            raise HealthValueError(amount)
        self._health -= amount
        if self._health <= 0:
            self.die()

    @abstractmethod
    def behave(self, ecosystem: "Ecosystem") -> list["Command"]:
        """Behave abstract method for all organisms

        :param: ecosystem: Ecosystem in which organism behaves.
        :type: Ecosystem
        :return: Commands to perform
        :rtype: list[Command]"""
        pass

    def get_older(self) -> None:
        self._age += 1
        # TODO: вывести в config magic numbers
        if self._energy > 50 and self._age <= 25:
            self._size += 0.5 * self._grow_rate
        if self._age > 25:
            self._health -= int(self._age / 25)

    def clone(self, **kwargs) -> "Organism":
        """
        Override this method if your subclass adds parameters to __init__.
        Call super().clone(**kwargs) and pass extra params via kwargs.(example in Animal class)
        """
        base_params = {
            "organism_id": kwargs.pop("organism_id", self._id),
            "name": kwargs.pop("name", self._name),
            "position": kwargs.pop("position", copy.copy(self._position)),
            "energy": STARTER_ENERGY,
            "health": STARTER_HEALTH,
            "age": 0,
            "size": self._size * 0.5,
            "grow_rate": self._grow_rate,
            **kwargs,
        }
        return type(self)(**base_params)

    # ?: подумать на счет логики размножения (нужен ли партнер)
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

    def clone(self, **kwargs) -> "Animal":
        kwargs.setdefault("hunger_rate", self._hunger_rate)
        kwargs.setdefault("vision_radius", self._vision_radius)
        kwargs.setdefault("speed", self._speed)
        return super().clone(**kwargs)

    def behave(self, ecosystem) -> list["Command"]:
        if not self.is_alive():
            return []
        commands: list["Command"] = []
        if random.random() <= SOUND_PRODUCTION_CHANCE:
            commands.append(self.make_sound())
        escape_command = self.suspect(ecosystem)
        if escape_command:
            commands.append(escape_command)
            return commands

        if self._energy <= MIN_ENERGY_TO_SEEK_FOOD:
            food_command = self.find_food(ecosystem)
            if food_command:
                commands.append(food_command)
                return commands
            else:
                commands.append(self.wander())
                return commands
        # TODO: добавить размножение

        if self._energy < COMFORT_ENERGY_LEVEL:
            commands.append(RestCommand(resting=self))
        else:
            commands.append(self.wander())

        return commands

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
            food_list, key=lambda f: self._position.distance_to(f.position)
        )

        dist = self._position.distance_to(closest_food.position)

        if dist <= MIN_DISTANCE_TO_EAT:
            return EatCommand(eater=self, food=closest_food)

        return MoveCommand(
            mover=self, target_position=closest_food.position, is_sprinting=True
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
            predators, key=lambda p: self._position.distance_to(p.position)
        )

        dx = self._position.x - closest_predator.position.x
        dy = self._position.y - closest_predator.position.y

        safe_pos = Position(self._position.x + dx, self._position.y + dy)

        return MoveCommand(mover=self, target_position=safe_pos, is_sprinting=True)

    def wander(self) -> "MoveCommand":
        random_x = self._position.x + random.uniform(-10, 10)
        random_y = self._position.y + random.uniform(-10, 10)
        target = Position(random_x, random_y)

        return MoveCommand(mover=self, target_position=target)

    def rest(self) -> "RestCommand":
        return RestCommand(resting=self)


# TODO: нивелировать метаболизм для растений через photosynthesis_rate
# TODO: добавить размножение
class Plant(Organism):
    def __init__(self, *, photosynthesis_rate: float, **kwargs):
        super().__init__(**kwargs)
        self._photosynthesis_rate = photosynthesis_rate

    @property
    def photosynthesis_rate(self):
        return self._photosynthesis_rate

    def clone(self, **kwargs) -> "Plant":
        kwargs.setdefault("photosynthesis_rate", self._photosynthesis_rate)
        return super().clone(**kwargs)

    def behave(self, ecosystem) -> list["Command"]:
        return [
            PhotosynthesisCommand(
                plant=self, photosynthesis_rate=self._photosynthesis_rate
            )
        ]
