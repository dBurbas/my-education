from abc import ABC, abstractmethod
from base import Position
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from organisms import Organism


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
