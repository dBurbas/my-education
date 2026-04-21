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

    def get_existing_sports(self):
        return list(set(athl.sport for athl in self._athletes if athl.sport))

    def get_existing_ranks(self):
        return list(set(athl.rank for athl in self._athletes if athl.rank))

    def get_total_athletes_count(self):
        return len(self._athletes)

    def add_athlete(self, athlete_obj: Athlete):
        self._athletes.append(athlete_obj)

    def remove_athletes(self, search_criteria):
        to_delete = list(self.find_athletes(search_criteria))
        for athlete in to_delete:
            self._athletes.remove(athlete)

        return len(to_delete)

    def find_athletes(self, search_criteria: dict):
        found = self._athletes
        for key, expected_value in search_criteria.items():
            if key in self._filter_rules:
                rule_func = self._filter_rules[key]
                found = [athl for athl in found if rule_func(athl, expected_value)]
            else:
                raise AthleteManagerError(f"Неизвестный критерий поиска: {key}")

        return found

    def sort_athletes(self, sort_criteria, reverse=False):
        if sort_criteria in self._sort_criterias.keys():
            sort_func = self._sort_criterias[sort_criteria]
            self._athletes = sort_func(self._athletes, reverse)
        else:
            raise AthleteManagerError(
                f"Неизвестный критерий сортировки: {sort_criteria}"
            )

    def clear_athletes(self):
        self._athletes.clear()

    # TODO: save_to_file
    def save_to_file(self, filepath: str):
        pass

    # TODO: load_from_file
    def load_from_file(self, filepath: str):
        pass
