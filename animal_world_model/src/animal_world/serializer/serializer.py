from abc import ABC, abstractmethod
import json
from src.animal_world.core.event_manager import EventManager
from src.animal_world.core.factory import OrganismFactory
from src.animal_world.core.ecosystem import Habitat, FoodChain, Ecosystem
from src.animal_world.exception.animal_world_exceptions import EcosystemLoadError


class ILoader(ABC):
    @abstractmethod
    def load(self, filepath: str):
        pass


class ISaver(ABC):
    @abstractmethod
    def save(self, data, filepath: str) -> None:
        pass


class JSONLoader(ILoader):
    def __init__(self, factory: OrganismFactory, encoding: str = "utf-8"):
        self._encoding = encoding
        self._factory = factory

    def load(self, filepath: str):
        with open(file=filepath, mode="r", encoding=self._encoding) as file:
            data: dict = json.load(file)
            if len(data) == 0 or not data["food_chain"] or not data["habitat"]:
                raise EcosystemLoadError("No needed data in file")
            habitat = Habitat.from_dict(data["habitat"])
            diet_rules = {}
            for eater_name, prey_names in data["food_chain"].items():
                eater_cls = self._factory.species_to_type(eater_name)
                prey_classes = [self._factory.species_to_type(p) for p in prey_names]
                diet_rules[eater_cls] = prey_classes

            food_chain = FoodChain(diet_rules=diet_rules)
            organisms = []
            for org_data in data["organisms"]:
                species_name = org_data.pop("type")
                name = org_data.pop("name")
                x = org_data.pop("x")
                y = org_data.pop("y")
                saved_id = org_data.pop("organism_id")

                org = self._factory.create_organism(
                    species=species_name,
                    name=name,
                    x=x,
                    y=y,
                    organism_id=saved_id,
                    **org_data,
                )
                organisms.append(org)
            return Ecosystem(
                event_manager=EventManager(),
                habitat=habitat,
                organisms=organisms,
                food_chain=food_chain,
                factory=self._factory,
            )


class JSONSaver(ISaver):
    def __init__(self, encoding="utf-8"):
        self._encoding = encoding

    def save(self, data: dict, filepath: str) -> None:
        with open(file=filepath, mode="w", encoding=self._encoding) as file:
            # ?: Нужно ли использовать skipkeys
            json.dump(data, file, ensure_ascii=False, indent=2)
