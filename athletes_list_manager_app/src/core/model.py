class AthleteModel:
    def __init__(self):
        self._athletes = []

        self.filter_rules = {
            "fio": lambda athlete, val: val.lower() in athlete["fio"].lower(),
            "sport": lambda athlete, val: athlete["sport"] == val,
            "rank": lambda athlete, val: athlete["rank"] == val,
            "min_titles": lambda athlete, val: athlete["titles"] >= val,
            "max_titles": lambda athlete, val: athlete["titles"] <= val,
        }

    # TODO: get page (нужна ли проверка что не больше itemов чем есть в модели)
    def get_page(self, page_num: int, items_per_page: int = 10):
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
