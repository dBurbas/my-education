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
        self._athletes: list[Athlete] = [
            Athlete(
                "Иванов Алексей Петрович",
                "БГТУ-Динамо",
                "нападающий",
                10,
                "Водное поло",
                "кмс",
            ),
            Athlete(
                "Смирнова Ольга Игоревна",
                "Минчанка",
                "связующий",
                1,
                "Волейбол",
                "мастер спорта",
            ),
            Athlete(
                "Козлов Дмитрий Васильевич",
                "Юни-Динамо",
                "защитник",
                4,
                "Футбол",
                "кмс",
            ),
            Athlete(
                "Петрова Анна Сергеевна",
                "Гродно-93",
                "центральная",
                15,
                "Баскетбол",
                "1-й юношеский",
            ),
            Athlete(
                "Васильев Игорь Николаевич",
                "Неман-Гродно",
                "вратарь",
                88,
                "Хоккей",
                "мастер спорта",
            ),
            Athlete(
                "Новикова Елена Андреевна",
                "Минск-2000",
                "разыгрывающий",
                7,
                "Баскетбол",
                "кмс",
            ),
            Athlete(
                "Морозов Павел Дмитриевич",
                "БГУ",
                "нападающий",
                11,
                "Волейбол",
                "мастер спорта",
            ),
            Athlete(
                "Волкова Татьяна Ивановна",
                "Динамо-Юни",
                "свободный",
                2,
                "Волейбол",
                "кмс",
            ),
            Athlete(
                "Соколов Максим Олегович",
                "Шахтер Солигорск",
                "полузащитник",
                8,
                "Футбол",
                "мастер спорта",
            ),
            Athlete(
                "Лебедева Ксения Романовна",
                "Брест",
                "нападающий",
                17,
                "Баскетбол",
                "кмс",
            ),
            Athlete(
                "Кузнецов Артем Викторович",
                "Гомель",
                "защитник",
                23,
                "Футбол",
                "1-й юношеский",
            ),
            Athlete(
                "Попова Мария Александровна",
                "Минск-МГУ",
                "вратарь",
                30,
                "Водное поло",
                "мастер спорта",
            ),
            Athlete(
                "Орлов Денис Игоревич",
                "Витебск",
                "центральный",
                14,
                "Волейбол",
                "кмс",
            ),
            Athlete(
                "Васильева Алина Петровна",
                "Могилев",
                "легкая",
                55,
                "Легкая атлетика",
                "мастер спорта",
            ),
            Athlete(
                "Жуков Никита Сергеевич",
                "БелАЗ",
                "нападающий",
                9,
                "Хоккей",
                "кмс",
            ),
            Athlete(
                "Михайлова Дарья Олеговна",
                "Гродно",
                "защитник",
                3,
                "Футбол",
                "1-й юношеский",
            ),
            Athlete(
                "Федоров Илья Андреевич",
                "БГЭУ",
                "связующий",
                6,
                "Волейбол",
                "кмс",
            ),
            Athlete(
                "Алексеева Полина Владимировна",
                "Минск",
                "разыгрывающий",
                12,
                "Баскетбол",
                "мастер спорта",
            ),
            Athlete(
                "Степанов Глеб Максимович",
                "Неман",
                "нападающий",
                19,
                "Водное поло",
                "кмс",
            ),
            Athlete(
                "Николаева Ева Дмитриевна",
                "Брест-93",
                "центральная",
                21,
                "Волейбол",
                "мастер спорта",
            ),
            Athlete(
                "Макаров Роман Иванович",
                "Динамо Брест",
                "вратарь",
                1,
                "Футбол",
                "мастер спорта",
            ),
            Athlete(
                "Вороньева Софья Павловна",
                "Минск-КПД",
                "нападающий",
                10,
                "Гандбол",
                "кмс",
            ),
            Athlete(
                "Григорьев Тимур Артемович",
                "Юни",
                "защитник",
                5,
                "Хоккей",
                "1-й юношеский",
            ),
            Athlete(
                "Павлова Валерия Константиновна",
                "Гомель-2000",
                "связующий",
                4,
                "Волейбол",
                "мастер спорта",
            ),
            Athlete(
                "Семенов Владислав Юрьевич",
                "Шахтер",
                "полузащитник",
                16,
                "Футбол",
                "кмс",
            ),
            Athlete(
                "Егорова Арина Олеговна",
                "БГУФК",
                "легкая",
                27,
                "Легкая атлетика",
                "мастер спорта",
            ),
            Athlete(
                "Крылов Даниил Сергеевич",
                "Минск-Динамо",
                "нападающий",
                13,
                "Баскетбол",
                "кмс",
            ),
            Athlete(
                "Беляева Кристина Романовна",
                "Витебск-ОблДЮСШ",
                "вратарь",
                22,
                "Гандбол",
                "1-й юношеский",
            ),
            Athlete(
                "Ильин Матвей Андреевич",
                "Гродно-93",
                "центральный",
                11,
                "Волейбол",
                "мастер спорта",
            ),
            Athlete(
                "Тарасова Милана Викторовна",
                "Могилев-Динамо",
                "разыгрывающий",
                8,
                "Баскетбол",
                "кмс",
            ),
            Athlete(
                "Захаров Кирилл Игоревич",
                "Брест",
                "защитник",
                66,
                "Хоккей",
                "мастер спорта",
            ),
            Athlete(
                "Белова Анастасия Петровна",
                "Юни-Динамо",
                "нападающий",
                18,
                "Водное поло",
                "кмс",
            ),
            Athlete(
                "Куликов Арсений Денисович",
                "Минск",
                "полузащитник",
                7,
                "Футбол",
                "1-й юношеский",
            ),
            Athlete(
                "Фролова Вероника Олеговна",
                "Гомель",
                "связующий",
                3,
                "Волейбол",
                "мастер спорта",
            ),
            Athlete(
                "Медведев Глеб Викторович",
                "БГТУ",
                "нападающий",
                15,
                "Гандбол",
                "кмс",
            ),
            Athlete(
                "Комарова Ульяна Сергеевна",
                "Неман",
                "легкая",
                41,
                "Легкая атлетика",
                "мастер спорта",
            ),
            Athlete(
                "Воронов Тимофей Артемович",
                "Шахтер Солигорск",
                "вратарь",
                31,
                "Футбол",
                "кмс",
            ),
            Athlete(
                "Савина Елизавета Дмитриевна",
                "Минск-2000",
                "защитник",
                9,
                "Баскетбол",
                "1-й юношеский",
            ),
            Athlete(
                "Коновалов Илья Михайлович",
                "Динамо Брест",
                "нападающий",
                17,
                "Хоккей",
                "мастер спорта",
            ),
        ]

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
