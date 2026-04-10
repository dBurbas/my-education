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
    HabitatMapValuesError,
)
from core.organisms import Animal, Plant

if TYPE_CHECKING:
    from commands import Command
    from organisms import Organism
    from factory import OrganismFactory
    from event_manager import EventManager


class FoodChain:
    """Encapsulates the diet rules of all species in the simulation.

    Diet rules are stored as a mapping from a predator type to the list
    of types it is allowed to eat.

    :param diet_rules: Mapping of predator class -> list of prey classes.
    :type diet_rules: dict[Type[Organism], list[Type[Organism]]]
    """

    def __init__(self, *, diet_rules: dict[Type["Organism"], list[Type["Organism"]]]):
        self._diet_rules = diet_rules

    @property
    def diet_rules(self):
        return self._diet_rules

    def can_eat(self, *, eater: "Organism", eaten: "Organism") -> bool:
        """Check whether one organism is allowed to eat another per the diet rules.

        :param eater: The organism that wants to eat.
        :type eater: Organism
        :param eaten: The organism that would be eaten.
        :type eaten: Organism
        :return: ``True`` if the eater's type has the eaten's type in its diet.
        :rtype: bool
        """
        if type(eater) not in self._diet_rules:
            return False
        return type(eaten) in self._diet_rules[type(eater)]

    # TODO: check if this method can be used elsewhere
    def get_diet(self, species: type) -> list[type]:
        """Return the list of prey types for a given species.

        :param species: The class of the queried species.
        :type species: type
        :return: List of prey types, or an empty list if no rule is defined.
        :rtype: list[type]
        """
        return self._diet_rules.get(species, [])

    # ?:  нужно ли переводить на enum или будет нарушать DRY(закодировано в diet_rules)
    def classify_organism(self, org: "Organism") -> str:
        """Classify an organism by its ecological role based on its diet.

        :param org: The organism to classify.
        :type org: Organism
        :return: One of ``"producer"``, ``"herbivore"``, ``"predator"``, or ``"omnivore"``.
        :rtype: str
        """
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
        """Add a new diet rule to the food chain.

        If the eater type already has rules, the prey type is appended to its list.
        If the eater type has no rules yet, a new entry is created.

        :param eater_type: The predator class.
        :type eater_type: Type[Organism]
        :param eaten_type: The prey class to add.
        :type eaten_type: Type[Organism]
        :raises FoodRuleAlreadyExistsError: If the rule already exists.
        """
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
        """Remove an existing diet rule from the food chain.

        :param eater_type: The predator class.
        :type eater_type: Type[Organism]
        :param eaten_type: The prey class to remove.
        :type eaten_type: Type[Organism]
        :raises FoodRuleNotFoundError: If the rule does not exist.
        """
        if (
            eater_type in self._diet_rules
            and eaten_type in self._diet_rules[eater_type]
        ):
            self._diet_rules[eater_type].remove(eaten_type)
        else:
            raise FoodRuleNotFoundError(eater_type, eaten_type)


class Habitat:
    """Represents the physical boundaries of the simulation space.

    :param map: A ``(width, height)`` tuple defining the maximum coordinates.
    :type map: tuple[float, float]
    """

    def __init__(self, map: tuple[float, float] = (10.0, 10.0)):
        x, y = map
        if x <= 0.0 or y <= 0.0:
            raise HabitatMapValuesError(x, y)
        self._max_x = x
        self._max_y = y

    @property
    def max_x(self):
        return self._max_x

    @property
    def max_y(self):
        return self._max_y

    def clamp_position(self, pos: Position) -> Position:
        """Clamp a position so it stays within the habitat boundaries.

        :param pos: The desired position, potentially out of bounds.
        :type pos: Position
        :return: A new position with coordinates clamped to ``[0, max_x]`` and ``[0, max_y]``.
        :rtype: Position
        """

        clamped_x = max(0.0, min(pos.x, self._max_x))
        clamped_y = max(0.0, min(pos.y, self._max_y))

        return Position(clamped_x, clamped_y)


class IEcosystem(ABC):
    """Abstract interface for the ecosystem.

    Defines the contract that any concrete ecosystem implementation must satisfy.
    Used for dependency inversion in the controller layer.
    """

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
    def get_all_organisms_stats(self) -> list[dict]:
        pass

    @abstractmethod
    def get_organism_stats_by_name(self, name: str) -> list[dict]:
        pass

    @abstractmethod
    def get_eco_balance(self) -> dict[str, int]:
        pass

    @abstractmethod
    def get_bio_diversity(self) -> float:
        pass


class Ecosystem(IEcosystem):
    """Concrete ecosystem implementation.

    Holds the organism list, habitat, food chain, factory, and event manager.
    Drives the simulation loop via :meth:`tick`.

    :param event_manager: The pub/sub event dispatcher.
    :type event_manager: EventManager
    :param habitat: The physical space with boundary constraints.
    :type habitat: Habitat
    :param organisms: Initial list of organisms.
    :type organisms: list[Organism]
    :param food_chain: Diet rules between species.
    :type food_chain: FoodChain
    :param factory: Factory used to create new organisms during reproduction.
    :type factory: OrganismFactory
    """

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
        """Advance the simulation by one step.

        Execution order per tick:

        1. Remove dead organisms from the list.
        2. Apply metabolism to every organism (may kill some by starvation).
        3. Collect behaviour commands from all living organisms.
        4. Execute all collected commands.
        5. Apply aging to all living organisms (may kill some by old age).
        """
        self._remove_dead()
        # TODO: add a put to an copy array of organisms
        all_commands: list["Command"] = self._collect_commands()

        self._execute_commands(all_commands)
        # ?: one cycle???
        self._apply_aging()

    def _remove_dead(self):
        """Filter out all organisms whose health has dropped to zero or below."""
        self._organisms = [org for org in self._organisms if org.is_alive()]

    def _collect_commands(self) -> list["Command"]:
        """Apply metabolism to every organism and collect their behaviour commands.

        Publishes a ``DIE_STARVATION_EVENT`` for any organism that dies during
        metabolism before commands are collected.

        :return: Flat list of all commands from all living organisms.
        :rtype: list[Command]
        """
        all_commands: list["Command"] = []
        for organism in self._organisms:
            organism.apply_metabolism()
            # ?: violation of SRP lines beneath
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
        """Execute every command in the provided list against this ecosystem.

        :param commands: Commands produced during the current tick.
        :type commands: list[Command]
        """
        for command in commands:
            command.execute(self)

    def _apply_aging(self):
        """Increment the age of every living organism and handle age-related death.

        Publishes a ``DIE_OLD_EVENT`` for any organism whose health drops to zero
        as a result of aging.

        .. note::
            Offspring spawned during the same tick will also age here.
            See the inline TODO for the planned fix.
        """
        # TODO: pass a list of organisms (old, so that the child doesn't immediately age after commands)
        for organism in self._organisms:
            if organism.is_alive():
                organism.get_older()
                # ?: violation of SRP lines beneath
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
        """Return all living organisms within a given radius of a position.

        The organism at ``center_pos`` itself (distance ≈ 0) is excluded.

        :param center_pos: The centre of the search area.
        :type center_pos: Position
        :param radius: Maximum distance from ``center_pos``.
        :type radius: float
        :return: List of living organisms within the radius.
        :rtype: list[Organism]
        """
        neighbors = []

        for org in self._organisms:
            if not org.is_alive():
                continue

            dist = center_pos.distance_to(org.position)

            if dist <= radius and dist > 0.0001:
                neighbors.append(org)

        return neighbors

    def add_organism(self, organism: "Organism"):
        """Add a new organism to the ecosystem.

        :param organism: The organism to add.
        :type organism: Organism
        :raises OrganismAlreadyDeadError: If the organism is already dead.
        :raises OrganismAlreadyExistsError: If an organism with the same ID already exists.
        """
        if not organism.is_alive():
            raise OrganismAlreadyDeadError(organism.organism_id)
        if any(org.organism_id == organism.organism_id for org in self._organisms):
            raise OrganismAlreadyExistsError(organism.organism_id)
        if (
            organism.position.x < 0
            or organism.position.x > self._habitat._max_x
            or organism.position.y < 0
            or organism.position.y > self._habitat.max_y
        ):
            raise OrganismException(
                "Position is not correct for this organism", organism.name
            )
        self._organisms.append(organism)

    def remove_organism(self, id_to_remove: int) -> bool:
        """Kill and remove a living organism by its ID.

        :param id_to_remove: The ID of the organism to remove.
        :type id_to_remove: int
        :return: ``True`` if the organism was found and killed.
        :rtype: bool
        :raises OrganismNotFoundError: If no living organism with that ID exists.
        """
        # ?: optimization maybe
        for org in self._organisms:
            if org.organism_id == id_to_remove and org.is_alive():
                org.die()
                return True
        raise OrganismNotFoundError(id_to_remove)

    # ? Нужно ли переводить с str -> type
    def get_population_stats(self) -> dict[str, int]:
        """Count living organisms grouped by their class name.

        :return: Mapping of class name -> count of living organisms of that type.
        :rtype: dict[str, int]
        """
        stats = {}
        for org in self.organisms:
            if org.is_alive():
                org_type = type(org).__name__
                stats[org_type] = stats.get(org_type, 0) + 1
        return stats

    def get_all_organisms_stats(self) -> list[dict]:
        """Retrieve detailed stats for every living organism in ecosystem.

        Name comparison is case-insensitive.

        :param name: The name to search for.
        :type name: str
        :return: List of dicts with keys ``name``, ``type``, ``health``, ``energy``,
                 ``age``, ``size``, ``x_cordinate``, ``y_cordinate``.
        :rtype: list[dict]
        """

        result = []
        for org in self._organisms:
            if org.is_alive():
                result.append(
                    {
                        "name": org.name,
                        "type": type(org).__name__,
                        "health": org.health,
                        "energy": org.energy,
                        "age": org.age,
                        "size": org.size,
                        "cord_x": org.position.x,
                        "cord_y": org.position.y,
                    }
                )
        return result

    def get_organism_stats_by_name(self, name: str) -> list[dict]:
        """Retrieve detailed stats for every living organism matching a name.

        Name comparison is case-insensitive.

        :param name: The name to search for.
        :type name: str
        :return: List of dicts with keys ``name``, ``type``, ``health``, ``energy``,
                 ``age``, ``size``, ``x_cordinate``, ``y_cordinate``.
        :rtype: list[dict]
        """

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
                        "cord_x": org.position.x,
                        "cord_y": org.position.y,
                    }
                )
        return result

    def get_eco_balance(self) -> dict[str, int]:
        """Count living organisms grouped by ecological role.

        Roles are determined by `FoodChain.classify_organism`.

        :return: Mapping with keys ``"producer"``, ``"herbivore"``, ``"predator"``,
                 ``"omnivore"`` and their counts.
        :rtype: dict[str, int]
        """
        counts = {"producer": 0, "herbivore": 0, "predator": 0, "omnivore": 0}
        for org in self._organisms:
            if org.is_alive():
                role = self.food_chain.classify_organism(org)
                counts[role] += 1
        return counts

    def get_bio_diversity(self) -> float:
        """Calculate the Margalef biodiversity index for the current ecosystem state.

        .. math::

            D = \\frac{S - 1}{\\ln N}

        where *S* is the number of distinct species and *N* is the total
        number of living organisms.

        :return: Margalef diversity index.
        :rtype: float
        :raises OrganismException: If there are no living organisms (division by zero).
        """
        species_count: int = 0
        organisms_count: int = 0
        population_stats: dict[str, int] = self.get_population_stats()
        for _, count in population_stats.items():
            species_count += 1
            organisms_count += count
        if organisms_count <= 1:
            raise OrganismException(
                "Non-correct organisms count(<=1), cannot calculate bio diversity"
            )
        diversity_index: float = (species_count - 1) / log(organisms_count)
        return diversity_index
