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
    """Abstract base class for all organisms in the simulation.

    Provides common state (energy, health, age, size) and behaviour interface.
    Subclasses must implement :meth:`behave`.

    :param organism_id: Unique integer identifier.
    :type organism_id: int
    :param name: Human-readable name.
    :type name: str
    :param position: Initial position in the habitat.
    :type position: Position
    :param energy: Starting energy level.
    :type energy: int
    :param health: Starting health level.
    :type health: int
    :param age: Starting age in ticks.
    :type age: int
    :param size: Initial physical size.
    :type size: float
    :param grow_rate: Multiplier applied to growth increments.
    :type grow_rate: float
    """

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
        """Increase energy by ``amount``, capped at ``MAX_ENERGY``.

        :param amount: Positive energy amount to add.
        :type amount: int
        :raises EnergyValueError: If ``amount`` is negative.
        """
        if amount < 0:
            raise EnergyValueError(amount)
        self._energy = min(self._energy + amount, MAX_ENERGY)

    def lose_energy(self, amount: int) -> None:
        """Decrease energy by ``amount``. Kills the organism if energy drops to zero or below.

        :param amount: Positive energy amount to subtract.
        :type amount: int
        :raises EnergyValueError: If ``amount`` is negative.
        """
        if amount < 0:
            raise EnergyValueError(amount)
        self._energy -= amount
        if self._energy <= 0:
            self.die()

    def move_to(self, pos: Position) -> None:
        """Teleport the organism to the given position.

        Called by :class:`~commands.MoveCommand` after boundary clamping.

        :param pos: The new position.
        :type pos: Position
        """
        self._position = pos

    def apply_metabolism(self) -> None:
        """Consume energy proportional to the organism's size each tick.

        Energy consumed = ``cost_of_living * size``. Kills the organism if
        energy drops to zero or below.
        """
        self._energy -= int(self._cost_of_living * (self._size))
        if self._energy <= 0:
            self.die()

    def grow(self, amount: int) -> None:
        """Increase the organism's size by ``amount``.

        :param amount: Non-negative growth increment.
        :type amount: int
        :raises GrowthValueError: If ``amount`` is negative.
        """
        if amount < 0:
            raise GrowthValueError(amount)
        self._size += amount

    def gain_health(self, amount: int) -> None:
        """Increase health by ``amount``, capped at ``MAX_HEALTH``.

        :param amount: Positive health amount to add.
        :type amount: int
        :raises HealthValueError: If ``amount`` is negative.
        """
        if amount < 0:
            raise HealthValueError(amount)
        self._health = min(self._health + amount, MAX_HEALTH)

    def lose_health(self, amount: int) -> None:
        """Decrease health by ``amount``. Kills the organism if health drops to zero or below.

        :param amount: Positive health amount to subtract.
        :type amount: int
        :raises HealthValueError: If ``amount`` is negative.
        """
        if amount < 0:
            raise HealthValueError(amount)
        self._health -= amount
        if self._health <= 0:
            self.die()

    @abstractmethod
    def behave(self, ecosystem: "Ecosystem") -> list["Command"]:
        """Behave abstract method for all organisms

        :param ecosystem: Ecosystem in which organism behaves.
        :type ecosystem: Ecosystem
        :return: Commands to perform
        :rtype: list[Command]"""
        pass

    def get_older(self) -> None:
        """Increment age by one tick and apply age-related effects.

        - While ``age <= 25`` and ``energy > 50``: size grows by ``0.5 * grow_rate``.
        - After age 25: health decreases by ``age // 25`` per tick.

        .. note::
            Magic numbers (25, 0.5, 50) should be moved to ``config.py``.
        """
        self._age += 1
        # TODO: вывести в config magic numbers
        if self._energy > 50 and self._age <= 25:
            self._size += 0.5 * self._grow_rate
        if self._age > 25:
            self._health -= int(self._age / 25)

    def clone(self, **kwargs) -> "Organism":
        """Create a new organism of the same type with starter stats (offspring).

        Base parameters (``organism_id``, ``name``, ``position``) can be overridden
        via ``kwargs``. The offspring starts with ``STARTER_ENERGY``, ``STARTER_HEALTH``,
        ``age=0``, and ``size = parent.size * 0.5``.

        Override this in subclasses that add new ``__init__`` parameters and call
        ``super().clone(**kwargs)``, injecting the extra params via ``kwargs``
        (see :class:`Animal` for an example).

        :return: A new organism instance of the same concrete type.
        :rtype: Organism
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

    # ?: thought: is sexual reproduction needed??
    def reproduce(self) -> "ReproduceCommand":
        """Create a :class:`~commands.ReproduceCommand` for this organism.

        :return: Command that will spawn an offspring when executed.
        :rtype: ReproduceCommand
        """
        return ReproduceCommand(reproducer=self)

    def is_alive(self) -> bool:
        """Check whether the organism is still alive.

        :return: ``True`` if health is greater than zero.
        :rtype: bool
        """
        return self._health > 0

    def die(self) -> None:
        """Kill the organism immediately by setting health to zero."""
        self._health = 0


class Animal(Organism):
    """Abstract base class for all animals.

    Extends :class:`Organism` with movement, vision, hunger, and sound capabilities.
    Provides a default decision-making loop in :meth:`behave`.

    :param hunger_rate: Rate at which the animal gets hungry (currently unused in metabolism — kept for future use).
    :type hunger_rate: float
    :param vision_radius: Radius in habitat units within which the animal can perceive others.
    :type vision_radius: float
    :param speed: Maximum distance the animal can travel per tick.
    :type speed: float
    """

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
        """Abstract make sound method.

        Should be overriden in the subclasses (see in :class:`~species.Wolf`)
        """
        pass

    def clone(self, **kwargs) -> "Animal":
        """Clone the animal, preserving ``hunger_rate``, ``vision_radius``, and ``speed``.

        :return: A new animal instance with starter stats.
        :rtype: Animal
        """
        kwargs.setdefault("hunger_rate", self._hunger_rate)
        kwargs.setdefault("vision_radius", self._vision_radius)
        kwargs.setdefault("speed", self._speed)
        return super().clone(**kwargs)

    def behave(self, ecosystem) -> list["Command"]:
        """Decide and return the list of commands for this tick.

        Priority order:

        1. Random chance to produce a sound.
        2. Flee from the nearest predator if one is visible (:meth:`suspect`).
        3. Seek and eat food if energy is low (:meth:`find_food`); wander if none found.
        4. Rest if energy is below ``COMFORT_ENERGY_LEVEL``; otherwise wander.

        :param ecosystem: The ecosystem context used to query neighbours and rules.
        :type ecosystem: Ecosystem
        :return: List of commands to execute.
        :rtype: list[Command]
        """
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
        """Locate the nearest edible organism and return a command to eat or approach it.

        Returns an :class:`~commands.EatCommand` if the food is within
        ``MIN_DISTANCE_TO_EAT``, otherwise a sprinting :class:`~commands.MoveCommand`
        towards it. Returns ``None`` if no food is visible.

        :param ecosystem: The ecosystem context.
        :type ecosystem: Ecosystem
        :return: An eat or move command, or ``None``.
        :rtype: Optional[Command]
        """
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
        """Check for nearby predators and return a flee command if one is found.

        Calculates an escape position by reflecting the animal's position away from
        the closest predator and returns a sprinting :class:`~commands.MoveCommand`.

        :param ecosystem: The ecosystem context.
        :type ecosystem: Ecosystem
        :return: A sprinting move command away from the closest predator, or ``None``.
        :rtype: Optional[Command]
        """
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
        """Return a move command to a random position within ±10 units of current position.

        :return: A non-sprinting :class:`~commands.MoveCommand`.
        :rtype: MoveCommand
        """
        random_x = self._position.x + random.uniform(-10, 10)
        random_y = self._position.y + random.uniform(-10, 10)
        target = Position(random_x, random_y)

        return MoveCommand(mover=self, target_position=target)

    def rest(self) -> "RestCommand":
        """Return a :class:`~commands.RestCommand` for this animal.

        :return: Rest command that restores energy and health.
        :rtype: RestCommand
        """
        return RestCommand(resting=self)


# TODO: нивелировать метаболизм для растений через photosynthesis_rate
class Plant(Organism):
    """Abstract base class for all plants.

    Plants do not move or make sounds. Each tick they perform photosynthesis,
    gaining energy and growing in size.

    :param photosynthesis_rate: Multiplier applied to the base photosynthesis gain.
    :type photosynthesis_rate: float
    """

    def __init__(self, *, photosynthesis_rate: float, **kwargs):
        super().__init__(**kwargs)
        self._photosynthesis_rate = photosynthesis_rate

    @property
    def photosynthesis_rate(self):
        return self._photosynthesis_rate

    def clone(self, **kwargs) -> "Plant":
        """Clone the plant, preserving ``photosynthesis_rate``.

        :return: A new plant instance with starter stats.
        :rtype: Plant
        """
        kwargs.setdefault("photosynthesis_rate", self._photosynthesis_rate)
        return super().clone(**kwargs)

    def behave(self, ecosystem) -> list["Command"]:
        """Return a single :class:`~commands.PhotosynthesisCommand` for this tick.

        :param ecosystem: The ecosystem context (unused directly but required by interface).
        :type ecosystem: Ecosystem
        :return: List containing one photosynthesis command.
        :rtype: list[Command]

        .. note::
            Need to add reproduction to behavior.
        """
        # TODO: добавить размножение
        return [
            PhotosynthesisCommand(
                plant=self, photosynthesis_rate=self._photosynthesis_rate
            )
        ]
