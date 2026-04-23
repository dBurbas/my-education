from abc import ABC, abstractmethod
import xml.dom.minidom as minidom
from core.athlete import Athlete


class ISaver(ABC):
    @abstractmethod
    def save(self, athletes: list[Athlete], filepath: str):
        pass


class DOMSaver(ISaver):
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding

    def save(self, athletes: list[Athlete], filepath: str):
        document = minidom.Document()

        root = document.createElement("athletes")
        document.appendChild(root)

        for athlete in athletes:
            athlete_node = document.createElement("athlete")

            def add_element(name, text_value):
                node = document.createElement(name)
                value = document.createTextNode(str(text_value))
                node.appendChild(value)
                athlete_node.appendChild(node)

            add_element("fio", athlete.fio)
            add_element("team", athlete.team)
            add_element("position", athlete.position)
            add_element("titles", athlete.titles)
            add_element("sport", athlete.sport)
            add_element("rank", athlete.rank)

            root.appendChild(athlete_node)

        with open(filepath, "w", encoding=self.encoding) as file:
            document.writexml(
                file, indent="  ", addindent="  ", newl="\n", encoding=self.encoding
            )
