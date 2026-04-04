from typing import Type, TYPE_CHECKING
from core.base import Position
from core.enums import EventType
from exception.animal_world_exceptions import (
    FoodRuleNotFoundError,
    FoodRuleAlreadyExistsError,
    OrganismAlreadyDeadError,
    OrganismAlreadyExistsError,
    OrganismNotFoundError,
)

if TYPE_CHECKING:
    from commands import Command
    from organisms import Organism
    from factory import OrganismFactory
    from event_manager import EventManager


# TODO: доработать все docstring
class FoodChain:
    """Class for diet rules of organisms"""

    def __init__(self, *, diet_rules: dict[Type["Organism"], list[Type["Organism"]]]):
        self._diet_rules = diet_rules

    def can_eat(self, *, eater: "Organism", eaten: "Organism") -> bool:
        if type(eater) not in self._diet_rules:
            raise FoodRuleNotFoundError(type(eater), type(eaten))
        return type(eaten) in self._diet_rules[type(eater)]

    def add_rule(
        self, *, eater_type: Type["Organism"], eaten_type: Type["Organism"]
    ) -> None:
        if eater_type in self._diet_rules:
            if eaten_type not in self._diet_rules[eater_type]:
                self._diet_rules[eater_type].append(eaten_type)
            else:
                raise FoodRuleAlreadyExistsError(eater_type, eaten_type)
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
        else:
            raise FoodRuleNotFoundError(eater_type, eaten_type)


class Habitat:
    def __init__(self, map: tuple[float, float] = (10.0, 10.0)):
        self._map = map

    def clamp_position(self, pos: Position) -> Position:
        """Clamps the position within the map boundaries"""
        max_x, max_y = self._map

        clamped_x = max(0.0, min(pos.x, max_x))
        clamped_y = max(0.0, min(pos.y, max_y))

        return Position(clamped_x, clamped_y)


class Ecosystem:
    def __init__(
        self,
        *,
        some_event_manager: "EventManager",
        some_habitat: "Habitat",
        some_organisms: list["Organism"],
        some_food_chain: "FoodChain",
        factory: "OrganismFactory",
    ):
        self._event_manager = some_event_manager
        self._habitat = some_habitat
        self._organisms = some_organisms
        self._food_chain = some_food_chain
        self._factory = factory

    # ? Нужны ли эти property
    @property
    def event_manager(self) -> "EventManager":
        return self._event_manager

    @property
    def habitat(self) -> "Habitat":
        return self._habitat

    @property
    def organisms(self) -> list["Organism"]:
        return self._organisms

    @property
    def food_chain(self) -> "FoodChain":
        return self._food_chain

    @property
    def factory(self) -> "OrganismFactory":
        return self._factory

    def tick(self):
        self._organisms = [org for org in self._organisms if org.is_alive()]
        all_commands: list["Command"] = []
        for organism in self.organisms:
            organism.apply_metabolism()
            # ?: не нарушает ли SRP строка ниже
            if not organism.is_alive():
                self._event_manager.publish(
                    EventType.DIE_EVENT,
                    {
                        "dead": organism.name,
                        "cause": EventType.DIE_STARVATION_EVENT,
                    },
                )
            if organism.is_alive():
                behavior: list["Command"] = organism.behave(self)
                all_commands.extend(behavior)

        for command in all_commands:
            command.execute(self)
        # ?: подумать о перемещении в один цикл
        for organism in self._organisms:
            if organism.is_alive():
                organism.get_older()
                # ?: не нарушает ли SRP строка ниже
                if not organism.is_alive():
                    self._event_manager.publish(
                        EventType.DIE_EVENT,
                        {
                            "dead": organism.name,
                            "cause": EventType.DIE_OLD_EVENT,
                        },
                    )

    def get_organisms_in_radius(
        self, center_pos: "Position", radius: float
    ) -> list["Organism"]:
        "Returns all living organisms within a given radius."
        neighbors = []

        for org in self._organisms:
            if not org.is_alive():
                continue

            dist = center_pos.distance_to(org._position)

            if dist <= radius and dist > 0.0001:
                neighbors.append(org)

        return neighbors

    def add_organism(self, organism: "Organism"):
        if not organism.is_alive():
            raise OrganismAlreadyDeadError(organism.organism_id)
        if any(org.organism_id == organism.organism_id for org in self._organisms):
            raise OrganismAlreadyExistsError(organism.organism_id)
        self._organisms.append(organism)

    def remove_organism(self, id_to_remove: int) -> bool:
        # ?: можно подумать на счет оптимизации
        for org in self._organisms:
            if org.organism_id == id_to_remove and org.is_alive():
                org.die()
                return True
        raise OrganismNotFoundError(id_to_remove)
