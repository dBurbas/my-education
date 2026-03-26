from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Type
from enums import EventType
import random
import copy


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


# TODO: проверять в каждой команде жив ли организм
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
        self._eater._energy = max(self._eater._energy + self._food._energy, 200)

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
        self._resting._energy += 10 if self._resting._energy < 200 else 0
        self._resting._health += 2
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
        self._cost_of_living = 1

    @abstractmethod
    # TODO: добавить отнятие энергии в зависимости от size и
    def behave(self, ecosystem: "Ecosystem") -> list["Command"]:
        """Behave abstract method for all organisms
        Args:
            ecosystem (Ecosystem): Ecosystem in which organism behaves.
        Returns:
            list[Command]: Commands to perform"""
        pass

    def is_alive(self) -> bool:
        return self._health > 0

    # TODO: подумать над логикой роста
    def grow(self) -> None:
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
        cloned_obj._energy = 100.0
        cloned_obj._health = 100.0

        return cloned_obj

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

    def find_food(self, ecosystem: "Ecosystem") -> "Command" | None:
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
            return EatCommand(predator=self, prey=closest_food)

        return MoveCommand(
            mover=self, target_pos=closest_food._position, is_sprinting=True
        )

    def suspect(self, ecosystem: "Ecosystem") -> "Command" | None:
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

        return MoveCommand(mover=self, target_pos=safe_pos, is_sprinting=True)

    def wander(self) -> MoveCommand:
        random_x = self._position.x + random.uniform(-10, 10)
        random_y = self._position.y + random.uniform(-10, 10)
        target = Position(random_x, random_y)

        return [MoveCommand(self, target)]

    def eat(self, pray: "Organism") -> EatCommand:
        return EatCommand(eater=self, food=pray)

    def rest(self) -> RestCommand:
        return RestCommand(self)


class Plant(Organism):
    def __init__(self, *, photosynthesis_rate: float, **kwargs):
        super().__init__(**kwargs)
        self._photosynthesis_rate = photosynthesis_rate

    def behave(self, ecosystem) -> list[Command]:

        return [
            PhotosynthesisCommand(
                plant=self, photosynthesis_rate=self._photosynthesis_rate
            )
        ]


class FoodChain:
    def __init__(self, *, diet_rules: dict[Type[Organism], list[Type[Organism]]]):
        self._diet_rules = diet_rules

    def can_eat(self, *, eater: Organism, eaten: Organism) -> bool:
        if type(eater) in self.diet_rules:
            return type(eaten) in self.diet_rules[type(eater)]

    def add_rule(
        self, *, eater_type: Type[Organism], eaten_type: Type[Organism]
    ) -> None:
        if eater_type in self._diet_rules:
            if eaten_type not in self._diet_rules[eater_type]:
                self._diet_rules[eater_type].append(eaten_type)
        else:
            self._diet_rules[eater_type] = [eaten_type]

    def remove_rule(
        self, *, eater_type: Type[Organism], eaten_type: Type[Organism]
    ) -> None:
        if (
            eater_type in self._diet_rules
            and eaten_type in self._diet_rules[eater_type]
        ):
            self._diet_rules[eater_type].remove(eaten_type)


class Habitat:
    # TODO: проверить класс
    map_size: tuple[float, float] = (10.0, 10.0)
    hide_rate: float
    success_hide_rate: float

    def get_hiding_bonus(self, animal_to_hide: Animal) -> float:
        return self.hide_rate

    def clamp_position(self, pos: Position) -> Position:
        """Clamps the position within the map boundaries"""
        max_x, max_y = self.map_size

        clamped_x = max(0.0, min(pos.x, max_x))
        clamped_y = max(0.0, min(pos.y, max_y))

        return Position(clamped_x, clamped_y)


class EventManager:
    pass


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


# TODO: сделать логику tick()
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
        for organism in self.organisms:
            behavior: list[Command] = organism.behave()
            for command in behavior:
                command.execute(self)

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
