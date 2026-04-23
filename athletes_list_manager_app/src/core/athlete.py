from dataclasses import dataclass


@dataclass
class Athlete:
    fio: str
    team: str
    position: str
    titles: int
    sport: str
    rank: str
