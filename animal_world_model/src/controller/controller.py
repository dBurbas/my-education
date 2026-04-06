from core.ecosystem import IEcosystem, FoodChain
from core.factory import OrganismFactory
from core.enums import EventType


class SimulationController:
    def __init__(
        self,
        ecosystem: IEcosystem,
        factory: OrganismFactory,
        food_chain: FoodChain,
    ):
        self._ecosystem = ecosystem
        self._factory = factory
        self._food_chain = food_chain
        self._event_logs = []
        self._step = 0
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Subscribes with event_manager"""
        em = self._ecosystem.event_manager
        em.subscribe(EventType.MOVE_EVENT, self._handle_move)
        em.subscribe(EventType.SOUND_EVENT, self._handle_sound)
        em.subscribe(EventType.REST_EVENT, self._handle_rest)
        em.subscribe(EventType.DIE_EVENT, self._handle_death)
        em.subscribe(EventType.REPRODUCTION_EVENT, self._handle_reproduction)
        em.subscribe(EventType.EAT_EVENT, self._handle_eat)

    # --- Handle events ---
    # TODO: добавить Photosynthese event
    # TODO: убрать форматирование строк в контроллере
    def _handle_rest(self, data: dict):
        self._event_logs.append(
            {
                "type": "rest",
                "animal": data.get("animal"),
                "health": data.get("health"),
                "energy": data.get("energy"),
            }
        )

    def _handle_move(self, data: dict):
        self._event_logs.append(
            {
                "type": "move",
                "mover": data.get("mover"),
                "x": data.get("new_position")[0],
                "y": data.get("new_position")[1],
            }
        )

    def _handle_sound(self, data: dict):
        self._event_logs.append(
            {
                "type": "sound",
                "sound_maker": data.get("sound_maker"),
                "sound": data.get("sound"),
            }
        )

    def _handle_death(self, data: dict):
        self._event_logs.append(
            {
                "type": "death",
                "name": data.get("dead"),
                "cause": data.get("cause"),
            }
        )

    def _handle_reproduction(self, data: dict):
        self._event_logs.append(
            {
                "type": "reproduction",
                "parent": data.get("parent"),
                "baby": data.get("baby"),
            }
        )

    def _handle_eat(self, data: dict):
        self._event_logs.append(
            {
                "type": "eat",
                "eater": data.get("eater"),
                "food": data.get("food"),
            }
        )

    # --- Methods for CLI ---
    def run_steps(self, steps: int):
        """Запускает симуляцию на N шагов"""
        for _ in range(steps):
            self._step += 1
            self._ecosystem.tick()

    def get_current_step(self) -> int:
        return self._step

    def get_latest_logs(self) -> list[dict]:
        """Возвращает логи последних событий и очищает их"""
        logs = self._event_logs.copy()
        self._event_logs.clear()
        return logs

    def get_population_stats(self) -> dict[str, int]:
        """Считает количество живых организмов по классам"""
        return self._ecosystem.get_population_stats()

    def get_available_species(self) -> list[str]:
        return self._factory.get_available_species()

    def get_food_chain(self):
        return self._food_chain._diet_rules

    def food_chain_add(self, eater: str, eaten: str):
        eater_type = self._factory.species_to_type(eater)
        eaten_type = self._factory.species_to_type(eaten)
        self._food_chain.add_rule(eater_type=eater_type, eaten_type=eaten_type)

    def food_chain_remove(self, eater: str, eaten: str):
        eater_type = self._factory.species_to_type(eater)
        eaten_type = self._factory.species_to_type(eaten)
        self._food_chain.remove_rule(eater_type=eater_type, eaten_type=eaten_type)

    def find_organisms_by_name(self, name: str) -> list[dict]:
        return [
            {"id": org.organism_id, "name": org.name, "type": type(org).__name__}
            for org in self._ecosystem.organisms
            if org.name.lower() == name.lower() and org.is_alive()
        ]

    def get_organism_stats(self, name: str) -> list[dict]:
        return self._ecosystem.get_organism_stats(name=name)

    def add_organism(
        self, species: str, name: str, x: float, y: float, **kwargs
    ) -> None:
        organism = self._factory.create_organism(species, name, x, y, **kwargs)
        self._ecosystem.add_organism(organism)

    def remove_organism(self, organism_id: int):
        self._ecosystem.remove_organism(id_to_remove=organism_id)

    def get_eco_balance(self) -> dict[str, int]:
        return self._ecosystem.get_eco_balance()

    def get_bio_diversity(self):
        return self._ecosystem.get_bio_diversity()
