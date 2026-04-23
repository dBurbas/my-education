from abc import ABC, abstractmethod
from core.athlete import Athlete
from xml import sax
from exceptions.athlete_manager_exceptions import AthleteManagerError


class ILoader(ABC):
    @abstractmethod
    def load(self, filepath: str) -> list[Athlete]:
        pass


class AthleteSAXHandler(sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.athletes: list[Athlete] = []
        self.current_tag = ""
        self.current_data = {}

    def startElement(self, tag, attributes):
        self.current_tag = tag
        if tag == "athlete":
            self.current_data = {}

    def characters(self, content):
        content = content.strip()
        if content and self.current_tag:
            if self.current_tag not in self.current_data:
                self.current_data[self.current_tag] = content
            else:
                self.current_data[self.current_tag] += content

    def endElement(self, tag):
        if tag == "athlete":
            try:
                athlete = Athlete(
                    fio=self.current_data.get("fio", ""),
                    team=self.current_data.get("team", ""),
                    position=self.current_data.get("position", ""),
                    titles=int(self.current_data.get("titles", 0)),
                    sport=self.current_data.get("sport", ""),
                    rank=self.current_data.get("rank", ""),
                )
                self.athletes.append(athlete)
            except ValueError as e:
                raise AthleteManagerError(f"Некорректные данные в XML: {e}")

        self.current_tag = ""


class SAXLoader(ILoader):
    def load(self, filepath: str) -> list[Athlete]:
        try:
            handler = AthleteSAXHandler()
            sax.parse(filepath, handler)
            return handler.athletes
        except FileNotFoundError:
            raise AthleteManagerError(f"Файл не найден: {filepath}")
        except PermissionError:
            raise AthleteManagerError(f"Нет прав доступа к файлу: {filepath}")
        except sax.SAXException as e:
            raise AthleteManagerError(f"Ошибка разбора XML: {e}")
