from core.ecosystem import Ecosystem
from core.enums import EventType
from rich.console import Console

console = Console()


class SimulationController:
    # TODO: перевести контроллер на абстрактную симуляцию
    def __init__(self, ecosystem: Ecosystem):
        self._ecosystem = ecosystem
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
    # TODO: убрать форматирование строк в контроллере
    def _handle_rest(self, data: dict):
        msg = f"[cyan]🐾 {data.get('animal')} rests, health: {data.get('health')}, energy:{data.get('energy')} [/cyan]"
        self._event_logs.append(msg)

    def _handle_move(self, data: dict):
        pos_x, pos_y = data.get("new_position")
        msg = f"[green]🐾 {data.get('mover')} moved to x:{pos_x}, y:{pos_y} [/green]"
        self._event_logs.append(msg)

    def _handle_sound(self, data: dict):
        msg = f"[blue]🔊 {data.get('sound_maker')} saying: {data.get('sound')}[/blue]"
        self._event_logs.append(msg)

    def _handle_death(self, data: dict):
        msg = f"[red]💀 Organism died: {data.get('dead')} {data.get('cause')}[/red]"
        self._event_logs.append(msg)

    def _handle_reproduction(self, data: dict):
        msg = f"[magenta]👶 Was born: {data.get('baby')} from {data.get('parent')}[/magenta]"
        self._event_logs.append(msg)

    def _handle_eat(self, data: dict):
        msg = f"[yellow]🍽️ {data.get('eater')} have eaten {data.get('food')}[/yellow]"
        self._event_logs.append(msg)

    # --- Methods for CLI ---
    def run_steps(self, steps: int):
        """Запускает симуляцию на N шагов"""
        for _ in range(steps):
            self._step += 1
            self._event_logs.append(f"Step: {self._step}")
            self._ecosystem.tick()

    def get_latest_logs(self) -> list[str]:
        """Возвращает логи последних событий и очищает их"""
        logs = self._event_logs.copy()
        self._event_logs.clear()
        return logs

    def get_population_stats(self) -> dict[str, int]:
        """Считает количество живых организмов по классам"""
        stats = {}
        for org in self._ecosystem.organisms:
            if org.is_alive():
                org_type = type(org).__name__
                stats[org_type] = stats.get(org_type, 0) + 1
        return stats

    # TODO: get_food_chain
    def get_food_chain(self):
        pass

    # TODO: add_food_chain
    def add_food_chain(self):
        pass

    # TODO: remove_food_chain
    def remove_food_chain(self):
        pass

    # TODO: get_organism_stats
    def get_organism_stats(self):
        pass

    # TODO: add_organism
    def add_organism(self):
        pass

    # TODO: add_organism
    def remove_organism(self):
        pass

    # TODO: get_eco_balance
    def get_eco_balance(self):
        pass

    # TODO: get_bio_diversity
    def get_bio_diversity(self):
        pass

    # TODO: save_to_file
    def save_to_file(self):
        pass

    # TODO: load_from_file
    def load_from_file(self):
        pass
