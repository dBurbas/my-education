from abc import ABC, abstractmethod
from core.base import Position
from typing import TYPE_CHECKING
from exception.animal_world_exceptions import UnknownSpeciesError
from core.species import Wolf, Rabbit, Fox, Grass

if TYPE_CHECKING:
    from organisms import Organism


class OrganismFactory(ABC):
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
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def create_offspring(self, parent: "Organism") -> "Organism":
        new_pos = Position(parent.position.x + 1, parent.position.y + 1)
        baby_id = self._get_id()
        baby = parent.clone(
            organism_id=baby_id, name=f"{parent.name} Jr. {baby_id}", position=new_pos
        )

        return baby

    def create_organism(
        self, species: str, name: str, x: float, y: float, **kwargs
    ) -> "Organism":
        cls = self._registry.get(species)
        if cls is None:
            raise UnknownSpeciesError(species)
        return cls(
            organism_id=self._get_id(), name=name, position=Position(x, y), **kwargs
        )

    def species_to_type(self, species: str) -> type["Organism"]:
        registry = self.get_registry()
        cls = registry.get(species)
        if cls is None:
            raise UnknownSpeciesError(species)
        return cls

    def get_registry(self) -> dict[str, type]:
        return dict(self._registry)

    def get_available_species(self) -> list[str]:
        return list(self._registry.keys())
