from typing import Type, TYPE_CHECKING
from abc import ABC, abstractmethod
from math import log
from core.base import Position
from core.enums import EventType
from exception.animal_world_exceptions import (
    OrganismException,
    FoodRuleNotFoundError,
    FoodRuleAlreadyExistsError,
    OrganismAlreadyDeadError,
    OrganismAlreadyExistsError,
    OrganismNotFoundError,
)
from core.organisms import Animal, Plant

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

    @property
    def diet_rules(self):
        return self._diet_rules

    def can_eat(self, *, eater: "Organism", eaten: "Organism") -> bool:
        if type(eater) not in self._diet_rules:
            return False
        return type(eaten) in self._diet_rules[type(eater)]

    # TODO: проверить можно ли где то еще использовать этот метод
    def get_diet(self, species: type) -> list[type]:
        return self._diet_rules.get(species, [])

    # ?:  нужно ли переводить на enum или будет нарушать DRY(закодировано в diet_rules)
    def classify_organism(self, org: "Organism") -> str:
        diet = self.get_diet(type(org))
        if not diet:
            return "producer"
        eats_animals = any(issubclass(prey, Animal) for prey in diet)
        eats_plants = any(issubclass(prey, Plant) for prey in diet)
        if eats_animals and eats_plants:
            return "omnivore"
        if eats_animals:
            return "predator"
        return "herbivore"

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


class IEcosystem(ABC):
    @property
    @abstractmethod
    def event_manager(self) -> "EventManager":
        pass

    @property
    @abstractmethod
    def organisms(self) -> list["Organism"]:
        pass

    @abstractmethod
    def tick(self) -> None:
        pass

    @abstractmethod
    def add_organism(self, organism: "Organism") -> None:
        pass

    @abstractmethod
    def remove_organism(self, organism_id: int) -> None:
        pass

    @abstractmethod
    def get_population_stats(self) -> dict[str, int]:
        pass

    @abstractmethod
    def get_organism_stats(self, name: str) -> list[dict]:
        pass

    @abstractmethod
    def get_eco_balance(self) -> dict[str, int]:
        pass

    @abstractmethod
    def get_bio_diversity(self) -> float:
        pass


class Ecosystem(IEcosystem):
    def __init__(
        self,
        *,
        event_manager: "EventManager",
        habitat: "Habitat",
        organisms: list["Organism"],
        food_chain: "FoodChain",
        factory: "OrganismFactory",
    ):
        self._event_manager = event_manager
        self._habitat = habitat
        self._organisms = organisms
        self._food_chain = food_chain
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
        self._remove_dead()
        # TODO: добавить выкладывание в массив организмов
        all_commands: list["Command"] = self._collect_commands()

        self._execute_commands(all_commands)
        # ?: подумать о перемещении в один цикл
        self._apply_aging()

    def _remove_dead(self):
        self._organisms = [org for org in self._organisms if org.is_alive()]

    def _collect_commands(self) -> list["Command"]:
        all_commands: list["Command"] = []
        for organism in self._organisms:
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
        return all_commands

    def _execute_commands(self, commands: list["Command"]):
        for command in commands:
            command.execute(self)

    # TODO: передавать список организмов(старый, чтобы после commands ребенок сразу не постарел)
    def _apply_aging(self):
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

            dist = center_pos.distance_to(org.position)

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

    # ? Нужно ли переводить с str на type
    def get_population_stats(self) -> dict[str, int]:
        """Counts the number of living organisms by class"""
        stats = {}
        for org in self.organisms:
            if org.is_alive():
                org_type = type(org).__name__
                stats[org_type] = stats.get(org_type, 0) + 1
        return stats

    def get_organism_stats(self, name: str) -> list[dict]:
        result = []
        for org in self._organisms:
            if org.name.lower() == name.lower() and org.is_alive():
                result.append(
                    {
                        "name": org.name,
                        "type": type(org).__name__,
                        "health": org.health,
                        "energy": org.energy,
                        "age": org.age,
                        "size": org.size,
                    }
                )
        return result

    def get_eco_balance(self) -> dict[str, int]:
        counts = {"producer": 0, "herbivore": 0, "predator": 0, "omnivore": 0}
        for org in self._organisms:
            if org.is_alive():
                role = self.food_chain.classify_organism(org)
                counts[role] += 1
        return counts

    def get_bio_diversity(self) -> float:
        """Calculate current biodiversity of the ecosystem (index Margalef)"""
        species_count: int = 0
        organisms_count: int = 0
        population_stats: dict[str, int] = self.get_population_stats()
        for _, count in population_stats.items():
            species_count += 1
            organisms_count += count
        if organisms_count == 0:
            raise OrganismException(
                "Zero organisms count, cannot calculate bio diversity"
            )
        diversity_index: float = (species_count - 1) / log(organisms_count)
        return diversity_index
