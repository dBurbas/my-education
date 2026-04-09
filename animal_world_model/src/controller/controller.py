from core.ecosystem import IEcosystem, FoodChain
from core.factory import OrganismFactory
from core.enums import EventType


class SimulationController:
    """Mediator between the ecosystem model and the CLI view.

    Subscribes to all ecosystem events, buffers them as log entries,
    and exposes a simplified API for the CLI layer.

    :param ecosystem: The ecosystem instance to control.
    :type ecosystem: IEcosystem
    :param factory: Factory used to create new organisms on demand.
    :type factory: OrganismFactory
    :param food_chain: The food chain being managed.
    :type food_chain: FoodChain
    """

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
        """Subscribe all internal event handlers to the ecosystem's EventManager."""
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
        """Handle a ``REST_EVENT`` and append it to the log buffer.

        :param data: Event payload with keys ``animal``, ``health``, ``energy``.
        :type data: dict
        """
        self._event_logs.append(
            {
                "type": "rest",
                "animal": data.get("animal"),
                "health": data.get("health"),
                "energy": data.get("energy"),
            }
        )

    def _handle_move(self, data: dict):
        """Handle a ``MOVE_EVENT`` and append it to the log buffer.

        :param data: Event payload with keys ``mover``, ``new_position`` (tuple), ``is_sprinting`` (bool).
        :type data: dict
        """
        # TODO: is_sprint
        self._event_logs.append(
            {
                "type": "move",
                "mover": data.get("mover"),
                "x": data.get("new_position")[0],
                "y": data.get("new_position")[1],
            }
        )

    def _handle_sound(self, data: dict):
        """Handle a ``SOUND_EVENT`` and append it to the log buffer.

        :param data: Event payload with keys ``sound_maker``, ``sound``.
        :type data: dict
        """
        self._event_logs.append(
            {
                "type": "sound",
                "sound_maker": data.get("sound_maker"),
                "sound": data.get("sound"),
            }
        )

    def _handle_death(self, data: dict):
        """Handle a ``DIE_EVENT`` and append it to the log buffer.

        :param data: Event payload with keys ``dead``, ``cause``.
        :type data: dict
        """
        self._event_logs.append(
            {
                "type": "death",
                "name": data.get("dead"),
                "cause": data.get("cause"),
            }
        )

    def _handle_reproduction(self, data: dict):
        """Handle a ``REPRODUCTION_EVENT`` and append it to the log buffer.

        :param data: Event payload with keys ``parent``, ``baby``.
        :type data: dict
        """
        self._event_logs.append(
            {
                "type": "reproduction",
                "parent": data.get("parent"),
                "baby": data.get("baby"),
            }
        )

    def _handle_eat(self, data: dict):
        """Handle an ``EAT_EVENT`` and append it to the log buffer.

        :param data: Event payload with keys ``eater``, ``food``.
        :type data: dict
        """
        self._event_logs.append(
            {
                "type": "eat",
                "eater": data.get("eater"),
                "food": data.get("food"),
            }
        )

    # --- Methods for CLI ---
    def run_steps(self, steps: int):
        """Run the simulation by the given number of ticks.

        :param steps: Number of simulation steps to run.
        :type steps: int
        """
        for _ in range(steps):
            self._step += 1
            self._ecosystem.tick()

    def get_current_step(self) -> int:
        """Return the total number of simulation ticks that have been executed.

        :return: Current simulation step count.
        :rtype: int
        """
        return self._step

    def get_latest_logs(self) -> list[dict]:
        """Return saved event logs and clear the internal buffer.

        :return: List of event log dicts collected since the last call.
        :rtype: list[dict]
        """
        logs = self._event_logs.copy()
        self._event_logs.clear()
        return logs

    def get_population_stats(self) -> dict[str, int]:
        """Return the count of living organisms grouped by species class name.

        :return: Mapping of class name -> living organism count.
        :rtype: dict[str, int]
        """
        return self._ecosystem.get_population_stats()

    def get_available_species(self) -> list[str]:
        """Return the list of species names available in the factory registry.

        :return: List of species name strings.
        :rtype: list[str]
        """
        return self._factory.get_available_species()

    def get_food_chain(self):
        """Return the raw diet rules dict from the food chain.

        :return: Mapping of predator type → list of prey types.
        :rtype: dict[Type[Organism], list[Type[Organism]]]
        """
        return self._food_chain.diet_rules

    def food_chain_add(self, eater: str, eaten: str):
        """Add a diet rule by species name strings.

        :param eater: Name of the predator species.
        :type eater: str
        :param eaten: Name of the prey species.
        :type eaten: str
        :raises UnknownSpeciesError: If either name is not in the factory registry.
        :raises FoodRuleAlreadyExistsError: If the rule already exists.
        """
        eater_type = self._factory.species_to_type(eater)
        eaten_type = self._factory.species_to_type(eaten)
        self._food_chain.add_rule(eater_type=eater_type, eaten_type=eaten_type)

    def food_chain_remove(self, eater: str, eaten: str):
        """Remove a diet rule by species name strings.

        :param eater: Name of the predator species.
        :type eater: str
        :param eaten: Name of the prey species.
        :type eaten: str
        :raises UnknownSpeciesError: If either name is not in the factory registry.
        :raises FoodRuleNotFoundError: If the rule does not exist.
        """
        eater_type = self._factory.species_to_type(eater)
        eaten_type = self._factory.species_to_type(eaten)
        self._food_chain.remove_rule(eater_type=eater_type, eaten_type=eaten_type)

    def find_organisms_by_name(self, name: str) -> list[dict]:
        """Find all living organisms whose name matches the given string (case-insensitive).

        :param name: The name to search for.
        :type name: str
        :return: List of dicts with keys ``id``, ``name``, ``type``.
        :rtype: list[dict]
        """
        return [
            {"id": org.organism_id, "name": org.name, "type": type(org).__name__}
            for org in self._ecosystem.organisms
            if org.name.lower() == name.lower() and org.is_alive()
        ]

    # TODO: get_all_organisms_stats
    def get_all_organisms_stats(self) -> list[dict]:
        """Return detailed stats for every living organism in ecosystem.

        :param name: The organism name to look up (case-insensitive).
        :type name: str
        :return: List of stat dicts (see :meth:`Ecosystem.get_all_organisms_stats`).
        :rtype: list[dict]
        """
        return self._ecosystem.get_all_organisms_stats()

    def get_organism_stats(self, name: str) -> list[dict]:
        """Return detailed stats for every living organism matching the given name.

        :param name: The organism name to look up (case-insensitive).
        :type name: str
        :return: List of stat dicts (see :meth:`Ecosystem.get_organism_stats_by_name`).
        :rtype: list[dict]
        """
        return self._ecosystem.get_organism_stats_by_name(name=name)

    def add_organism(
        self, species: str, name: str, x: float, y: float, **kwargs
    ) -> None:
        """Create and add a new organism to the ecosystem.

        :param species: Species name (must be in the factory registry).
        :type species: str
        :param name: Human-readable name for the organism.
        :type name: str
        :param x: X coordinate for the spawn position.
        :type x: float
        :param y: Y coordinate for the spawn position.
        :type y: float
        :param kwargs: Extra keyword arguments forwarded to the species constructor.
        """
        organism = self._factory.create_organism(species, name, x, y, **kwargs)
        self._ecosystem.add_organism(organism)

    def remove_organism(self, organism_id: int):
        """Kill and remove a living organism by its ID.

        :param organism_id: The ID of the organism to remove.
        :type organism_id: int
        :raises OrganismNotFoundError: If no living organism with that ID exists.
        """
        self._ecosystem.remove_organism(id_to_remove=organism_id)

    def get_eco_balance(self) -> dict[str, int]:
        """Return the count of living organisms grouped by ecological role.

        :return: Mapping with keys ``"producer"``, ``"herbivore"``, ``"predator"``,
                 ``"omnivore"`` and their respective counts.
        :rtype: dict[str, int]
        """
        return self._ecosystem.get_eco_balance()

    def get_bio_diversity(self):
        """Return the Margalef biodiversity index for the current ecosystem state.

        :return: Biodiversity index value.
        :rtype: float
        :raises OrganismException: If the ecosystem has no living organisms.
        """
        return self._ecosystem.get_bio_diversity()

    def get_traits(self, species: str) -> dict:
        return self._factory.get_traits(species)
