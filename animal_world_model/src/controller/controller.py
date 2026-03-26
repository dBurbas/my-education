from core.ecosystem import Ecosystem
from core.enums import EventType
from rich.console import Console

console = Console()


class SimulationController:
    def __init__(self, ecosystem: Ecosystem):
        self.ecosystem = ecosystem
        self._event_logs = []

        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Subscribes with event_manager"""
        em = self.ecosystem.event_manager
        em.subscribe(EventType.SOUND_EVENT, self._handle_sound)
        em.subscribe(EventType.DIE_EVENT, self._handle_death)
        em.subscribe(EventType.REPRODUCTION_EVENT, self._handle_reproduction)
        em.subscribe(EventType.EAT_EVENT, self._handle_eat)

    # --- Handle events ---
    def _handle_sound(self, data: dict):
        msg = f"[blue]🔊 {data.get('sound_maker')} saying: {data.get('sound')}[/blue]"
        self._event_logs.append(msg)

    def _handle_death(self, data: dict):
        msg = f"[red]💀 Organism died: {data.get('dead')}[/red]"
        self._event_logs.append(msg)

    def _handle_reproduction(self, data: dict):
        msg = f"[pink]👶 Was born: {data.get('baby')} from {data.get('parent')}[/pink]"
        self._event_logs.append(msg)

    def _handle_eat(self, data: dict):
        msg = f"[yellow]🍽️ {data.get('eater')} have eaten {data.get('food')}[/yellow]"
        self._event_logs.append(msg)

    # --- Methods for CLI ---
    def run_steps(self, steps: int):
        """Запускает симуляцию на N шагов"""
        for _ in range(steps):
            self.ecosystem.tick()

    def get_latest_logs(self) -> list[str]:
        """Возвращает логи последних событий и очищает их"""
        logs = self._event_logs.copy()
        self._event_logs.clear()
        return logs

    def get_population_stats(self) -> dict[str, int]:
        """Считает количество живых организмов по классам"""
        stats = {}
        for org in self.ecosystem.organisms:
            if org.is_alive():
                org_type = type(org).__name__
                stats[org_type] = stats.get(org_type, 0) + 1
        return stats
