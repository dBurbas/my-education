from math import ceil
from dataclasses import dataclass
from typing import Callable, Any
from exceptions.athlete_manager_exceptions import AthleteManagerError


@dataclass
class Athlete:
    fio: str
    team: str
    position: str
    titles: int
    sport: str
    rank: str


class AthleteManagerModel:
    def __init__(self):
        self._athletes: list[Athlete] = []

        self._filter_rules: dict[str, Callable[[Athlete, Any], bool]] = {
            "fio": lambda athlete, val: val.lower() in athlete.fio.lower(),
            "sport": lambda athlete, val: athlete.sport == val,
            "rank": lambda athlete, val: athlete.rank == val,
            "min_titles": lambda athlete, val: athlete.titles >= val,
            "max_titles": lambda athlete, val: athlete.titles <= val,
        }
        self._rank_weights: dict[str, int] = {
            "1-й юношеский": 1,
            "2-й разряд": 2,
            "3й-разряд": 3,
            "кмс": 4,
            "мастер спорта": 5,
        }
        self._sort_criterias: dict[
            str, Callable[[list[Athlete], bool], list[Athlete]]
        ] = {
            "fio": lambda athletes, rev: sorted(
                athletes, key=lambda a: a.fio, reverse=rev
            ),
            "titles": lambda athletes, rev: sorted(
                athletes, key=lambda a: a.titles, reverse=rev
            ),
            "rank": lambda athletes, rev: sorted(
                athletes,
                key=lambda a: self._rank_weights.get(a.rank, 0),
                reverse=rev,
            ),
        }

    def get_total_pages_num(self, items_per_page: int = 10) -> int:
        return max(1, ceil(len(self._athletes) / items_per_page))

    def get_page(self, page_num: int, items_per_page: int = 10) -> list[Athlete]:
        start: int = page_num * items_per_page
        return self._athletes[start : start + items_per_page]

    # TODO: get existing sports
    def get_existing_sports(self):
        pass

    # TODO: get existing ranks
    def get_existing_ranks(self):
        pass

    # TODO: add athlete
    def add_athlete(self, data):
        self._athletes.append(data)

    # TODO: remove athletes
    def remove_athletes(self):
        pass

    # TODO: find athletes
    def find_athletes(self):
        pass

    # TODO: sort athletes
    def sort_athletes(self):
        pass
