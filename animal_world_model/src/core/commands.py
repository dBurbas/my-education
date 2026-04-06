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
    """Abstract base class for all commands"""

    @abstractmethod
    def execute(self, ecosystem: "Ecosystem") -> None:
        pass


class EatCommand(Command):
    """Eat command class"""

    def __init__(self, *, eater: "Organism", food: "Organism"):
        self._eater = eater
        self._food = food

    def execute(self, ecosystem: "Ecosystem") -> None:
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
    """Photosynthesis command class"""

    def __init__(self, *, plant: "Plant", photosynthesis_rate: float):
        self._photosynthesis_rate = photosynthesis_rate
        self._plant = plant

    def execute(self, ecosystem: "Ecosystem") -> None:
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
    """Move command class"""

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
    """Rest command class"""

    def __init__(self, resting: "Organism"):
        self._resting = resting

    def execute(self, ecosystem: "Ecosystem") -> None:
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


# ?: нужно ли делать парное размножение???
class ReproduceCommand(Command):
    """Reproduce command class"""

    def __init__(self, *, reproducer: "Organism"):
        self._reproducer = reproducer

    def execute(self, ecosystem: "Ecosystem") -> None:
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
    """Sound command class"""

    def __init__(self, *, sound_maker: "Organism", sound: str):
        self._sound_maker = sound_maker
        self._sound = sound

    def execute(self, ecosystem: "Ecosystem") -> None:
        if not self._sound_maker.is_alive():
            return
        ecosystem.event_manager.publish(
            EventType.SOUND_EVENT,
            {"sound_maker": self._sound_maker.name, "sound": self._sound},
        )
