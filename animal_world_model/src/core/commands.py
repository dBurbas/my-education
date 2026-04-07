from core.enums import EventType
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from core.base import Position
from config import (
    ENERGY_ADD,
    HEALTH_ADD,
    REPRODUCTION_ENERGY_COST,
    REPRODUCTION_MIN_ENERGY,
    SPRINT_SPEED_MULTIPLIER,
    SPRINT_ENERGY_MULTIPLIER,
    BASE_MOVE_COST,
    PLANT_GROWTH_MULTIPLIER,
    PLANT_ENERGY_REWARD,
)

if TYPE_CHECKING:
    from organisms import Organism, Plant, Animal
    from ecosystem import Ecosystem


# TODO: доработать все docstring
class Command(ABC):
    """Abstract base class for all simulation commands (Command pattern).

    Every concrete command encapsulates a single action (eat, move, rest, etc.)
    and is executed by the current :class:`~ecosystem.Ecosystem` instance.
    """

    @abstractmethod
    def execute(self, ecosystem: "Ecosystem") -> None:
        pass


class EatCommand(Command):
    """Command that makes one organism eat another.

    The action is skipped if the eater is dead, the food is dead, the food chain
    forbids this pairing, or the eater is smaller than the food.

    On success: food dies, eater gains the food's energy, and both a
    ``EAT_EVENT`` and a ``DIE_EATEN_EVENT`` are published.

    :param eater: The organism performing the eating.
    :type eater: Organism
    :param food: The organism being eaten.
    :type food: Organism
    """

    def __init__(self, *, eater: "Organism", food: "Organism"):
        self._eater = eater
        self._food = food

    def execute(self, ecosystem: "Ecosystem") -> None:
        """Execute the eat action.

        :param ecosystem: Current ecosystem instance.
        :type ecosystem: Ecosystem
        """
        if (
            not self._eater.is_alive()
            or not ecosystem.food_chain.can_eat(eater=self._eater, eaten=self._food)
            or self._eater.size < self._food.size
            or not self._food.is_alive()
        ):
            return
        self._food.die()
        self._eater.gain_energy(self._food.energy)
        ecosystem.event_manager.publish(
            EventType.EAT_EVENT, {"eater": self._eater.name, "food": self._food.name}
        )
        ecosystem.event_manager.publish(
            EventType.DIE_EVENT,
            {"dead": self._food.name, "cause": EventType.DIE_EATEN_EVENT},
        )


class PhotosynthesisCommand(Command):
    """Command that triggers photosynthesis for a plant.

    Calculates an energy increase based on ``PLANT_GROWTH_MULTIPLIER``
    and ``photosynthesis_rate``, grows the plant, and publishes a
    ``PHOTOSYNTHESIS_EVENT``.

    .. warning::
        The energy increase is cast to ``int``, silently truncating float values.
        See inline TODO.

    :param plant: The plant performing photosynthesis.
    :type plant: Plant
    :param photosynthesis_rate: The rate at which photosynthesis occurs.
    :type photosynthesis_rate: float
    """

    def __init__(self, *, plant: "Plant", photosynthesis_rate: float):
        self._photosynthesis_rate = photosynthesis_rate
        self._plant = plant

    def execute(self, ecosystem: "Ecosystem") -> None:
        """Execute the photosynthesis action.

        :param ecosystem: Current ecosystem instance.
        :type ecosystem: Ecosystem
        """
        if not self._plant.is_alive():
            return
        # TODO: пофиксить проблему неявного преобразования энергии в float
        increase = int(PLANT_GROWTH_MULTIPLIER * self._photosynthesis_rate)
        self._plant.grow(increase)

        self._plant.gain_energy(increase * PLANT_ENERGY_REWARD)
        ecosystem.event_manager.publish(
            EventType.PHOTOSYNTHESIS_EVENT,
            {"plant": self._plant, "increase": increase},
        )


class MoveCommand(Command):
    """Command that moves an animal towards a target position.

    Movement is capped by the animal's speed. If sprinting, speed is multiplied
    by ``SPRINT_SPEED_MULTIPLIER`` and energy cost by ``SPRINT_ENERGY_MULTIPLIER``.
    The resulting position is clamped to habitat boundaries.

    The command is skipped if the animal is dead or has insufficient energy.

    :param mover: The animal to move.
    :type mover: Animal
    :param target_position: The desired destination.
    :type target_position: Position
    :param is_sprinting: Whether to sprint (higher speed, higher energy cost).
    :type is_sprinting: bool
    """

    def __init__(
        self,
        *,
        mover: "Animal",
        target_position: Position,
        is_sprinting: bool = False,
    ):
        self._mover = mover
        self._target_pos = target_position
        self._is_sprinting = is_sprinting

    def execute(self, ecosystem: "Ecosystem") -> None:
        """Execute the move action.

        :param ecosystem: Current ecosystem instance.
        :type ecosystem: Ecosystem
        """
        if (
            not self._mover.is_alive()
            or (
                self._is_sprinting
                and self._mover.energy < SPRINT_ENERGY_MULTIPLIER * BASE_MOVE_COST
            )
            or (not self._is_sprinting and self._mover.energy < BASE_MOVE_COST)
        ):
            return
        current_speed = self._mover.speed
        energy_cost = BASE_MOVE_COST

        if self._is_sprinting:
            current_speed *= SPRINT_SPEED_MULTIPLIER
            energy_cost *= SPRINT_ENERGY_MULTIPLIER

        current_pos = self._mover.position
        dist = current_pos.distance_to(self._target_pos)

        if dist <= 0.0001 or current_speed <= 0:
            return

        if dist > current_speed:
            ratio = current_speed / dist
            new_x = current_pos.x + (self._target_pos.x - current_pos.x) * ratio
            new_y = current_pos.y + (self._target_pos.y - current_pos.y) * ratio
            desired_pos = Position(new_x, new_y)
        else:
            desired_pos = self._target_pos

        final_pos = ecosystem.habitat.clamp_position(desired_pos)

        self._mover.move_to(final_pos)
        self._mover.lose_energy(energy_cost)

        ecosystem.event_manager.publish(
            EventType.MOVE_EVENT,
            {
                "mover": self._mover.name,
                "new_position": (final_pos.x, final_pos.y),
                "is_sprinting": self._is_sprinting,
            },
        )


class RestCommand(Command):
    """Command that makes an organism rest, recovering energy and health.

    On execution: organism gains ``ENERGY_ADD`` energy and ``HEALTH_ADD`` health,
    then a ``REST_EVENT`` is published.

    :param resting: The organism that is resting.
    :type resting: Organism
    """

    def __init__(self, resting: "Organism"):
        self._resting = resting

    def execute(self, ecosystem: "Ecosystem") -> None:
        """Execute the rest action.

        :param ecosystem: Current ecosystem instance.
        :type ecosystem: Ecosystem
        """
        if not self._resting.is_alive():
            return
        self._resting.gain_energy(ENERGY_ADD)
        self._resting.gain_health(HEALTH_ADD)
        ecosystem.event_manager.publish(
            EventType.REST_EVENT,
            {
                "animal": self._resting.name,
                "health": self._resting.health,
                "energy": self._resting.energy,
            },
        )


# ?: is sexual reproduction needed???
class ReproduceCommand(Command):
    """Command that makes an organism reproduce asexually.

    The action is skipped if the organism's energy is below
    ``REPRODUCTION_MIN_ENERGY``. On success: a new offspring is added to the
    ecosystem, the parent loses ``REPRODUCTION_ENERGY_COST`` energy, and a
    ``REPRODUCTION_EVENT`` is published.

    :param reproducer: The organism that is reproducing.
    :type reproducer: Organism
    """

    def __init__(self, *, reproducer: "Organism"):
        self._reproducer = reproducer

    def execute(self, ecosystem: "Ecosystem") -> None:
        """Execute the reproduction action.

        :param ecosystem: Current ecosystem instance.
        :type ecosystem: Ecosystem
        """
        if self._reproducer.energy < REPRODUCTION_MIN_ENERGY:
            return
        baby = ecosystem.factory.create_offspring(parent=self._reproducer)
        ecosystem.add_organism(baby)
        self._reproducer.lose_energy(REPRODUCTION_ENERGY_COST)
        ecosystem.event_manager.publish(
            EventType.REPRODUCTION_EVENT,
            {"parent": self._reproducer.name, "baby": baby.name},
        )


class SoundCommand(Command):
    """Command that makes an organism emit a sound.

    Publishes a ``SOUND_EVENT`` with the maker's name and the sound string.
    The action is skipped if the organism is dead.

    :param sound_maker: The organism producing the sound.
    :type sound_maker: Organism
    :param sound: The sound string (example: ``"Awoooooof"``).
    :type sound: str
    """

    def __init__(self, *, sound_maker: "Organism", sound: str):
        self._sound_maker = sound_maker
        self._sound = sound

    def execute(self, ecosystem: "Ecosystem") -> None:
        """Execute the sound action.

        :param ecosystem: Current ecosystem instance.
        :type ecosystem: Ecosystem
        """
        if not self._sound_maker.is_alive():
            return
        ecosystem.event_manager.publish(
            EventType.SOUND_EVENT,
            {"sound_maker": self._sound_maker.name, "sound": self._sound},
        )
