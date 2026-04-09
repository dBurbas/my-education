from abc import ABC, abstractmethod
from core.base import Position
from typing import TYPE_CHECKING
from exception.animal_world_exceptions import UnknownSpeciesError
from core.species import Wolf, Rabbit, Fox, Grass

if TYPE_CHECKING:
    from organisms import Organism


class OrganismFactory(ABC):
    """Abstract factory for creating organisms.

    Defines the interface for organism construction and species registration.
    """

    @abstractmethod
    def create_offspring(self, parent: "Organism") -> "Organism":
        pass

    @abstractmethod
    def create_organism(
        self, species: str, name: str, x: float, y: float, **kwargs
    ) -> "Organism":
        pass

    @abstractmethod
    def get_registry(self) -> dict[str, type]:
        pass

    @abstractmethod
    def species_to_type(self, species: str) -> type["Organism"]:
        pass

    @abstractmethod
    def get_available_species(self) -> list[str]:
        pass


class DefaultOrganismFactory(OrganismFactory):
    """Default factory implementation with a static species registry.

    Manages auto-incrementing IDs and supports creating organisms by name
    or as offspring of an existing parent.

    :param start_id: The first ID to assign to a newly created organism.
    :type start_id: int
    """

    # TODO: обновить реестр доступных видов
    _registry: dict[str, type] = {
        "Wolf": Wolf,
        "Rabbit": Rabbit,
        "Fox": Fox,
        "Grass": Grass,
    }

    def __init__(self, start_id: int = 1):
        self._next_id = start_id

    # ?: нужен ли генератор
    def _get_id(self) -> int:
        """Return the next available unique organism ID and increment the counter.

        :return: A unique integer ID.
        :rtype: int
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def create_offspring(self, parent: "Organism") -> "Organism":
        """Create an offspring of the given parent organism.

        The offspring is placed one unit diagonally from the parent and assigned
        the next available ID. Name is set to ``"<parent_name> Jr. <id>"``.

        :param parent: The parent organism to clone.
        :type parent: Organism
        :return: A new organism of the same type with starter stats.
        :rtype: Organism

        """
        import random

        offset_x = random.uniform(-3.0, 3.0)
        offset_y = random.uniform(-3.0, 3.0)
        new_pos = Position(parent.position.x + offset_x, parent.position.y + offset_y)
        baby_id = self._get_id()
        baby = parent.clone(
            organism_id=baby_id, name=f"{parent.name} Jr. {baby_id}", position=new_pos
        )

        return baby

    def create_organism(
        self, species: str, name: str, x: float, y: float, **kwargs
    ) -> "Organism":
        """Create a new organism of the given species at the specified position.

        :param species: The species name (must match a key in the registry).
        :type species: str
        :param name: Human-readable name for the new organism.
        :type name: str
        :param x: X coordinate in the habitat.
        :type x: float
        :param y: Y coordinate in the habitat.
        :type y: float
        :param kwargs: Additional keyword arguments forwarded to the species constructor.
        :raises UnknownSpeciesError: If ``species`` is not in the registry.
        :return: A new organism instance.
        :rtype: Organism
        """
        cls = self._registry.get(species)
        if cls is None:
            raise UnknownSpeciesError(species)
        return cls(
            organism_id=self._get_id(), name=name, position=Position(x, y), **kwargs
        )

    def species_to_type(self, species: str) -> type["Organism"]:
        """Resolve a species name string to its corresponding class.

        :param species: The species name to look up.
        :type species: str
        :return: The class registered under that name.
        :rtype: type[Organism]
        :raises UnknownSpeciesError: If ``species`` is not in the registry.
        """
        registry = self.get_registry()
        cls = registry.get(species)
        if cls is None:
            raise UnknownSpeciesError(species)
        return cls

    def get_registry(self) -> dict[str, type]:
        """Return a shallow copy of the species registry.

        :return: Mapping of species name -> class.
        :rtype: dict[str, type]
        """
        return dict(self._registry)

    def get_available_species(self) -> list[str]:
        """Return the list of registered species names.

        :return: List of species name strings.
        :rtype: list[str]
        """
        return list(self._registry.keys())
