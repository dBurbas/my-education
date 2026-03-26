from enums import EventType
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from base import Position

if TYPE_CHECKING:
    from organisms import Organism, Plant, Animal
    from ecosystem import Ecosystem
    from commands import Command


# TODO: доработать все docstring
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
        if (
            not self._eater.is_alive()
            or not ecosystem.food_chain.can_eat(eater=self._eater, eaten=self._food)
            or self._eater._size < self._food._size
            or not self._food.is_alive()
        ):
            return
        self._food.die()
        self._eater._energy = min(self._eater._energy + self._food._energy, 200)

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
        if not self._plant.is_alive():
            return
        increase = 0.5 * self._photosynthesis_rate
        self._plant._size += increase * 0.5
        self._plant._energy += increase * 10
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
        if not self._mover.is_alive() or self._mover._energy < 3:
            return
        current_speed = self._mover._speed
        energy_cost = 1

        if self._is_sprinting:
            current_speed *= 2
            energy_cost *= 3

        current_pos = self._mover._position
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

        self._mover._position = final_pos
        self._mover._energy -= energy_cost

        ecosystem.event_manager.publish(
            EventType.MOVE_EVENT,
            {"animal": self._mover._name, "new_position": (final_pos.x, final_pos.y)},
        )


class RestCommand(Command):
    """Rest command class"""

    def __init__(self, resting: "Organism"):
        self._resting = resting

    def execute(self, ecosystem: "Ecosystem") -> None:
        if not self._resting.is_alive():
            return
        self._resting._energy = min(self._resting._energy + 10, 200)
        self._resting._health = min(self._resting._health + 2, 100)
        ecosystem.event_manager.publish(
            EventType.REST_EVENT,
            {
                "animal": self._resting._name,
                "health": self._resting._health,
                "energy": self._resting._energy,
            },
        )


class ReproduceCommand(Command):
    """Reproduce command class"""

    def __init__(self, *, reproducer: "Organism"):
        self._reproducer = reproducer

    def execute(self, ecosystem: "Ecosystem") -> None:
        if self._reproducer._energy < 150:
            return
        baby = ecosystem.factory.create_offspring(parent=self._reproducer)
        ecosystem.organisms.append(baby)
        self._reproducer._energy -= 100
        ecosystem.event_manager.publish(
            EventType.REPRODUCTION_EVENT,
            {"parent": self._reproducer._name, "baby": baby._name},
        )


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
