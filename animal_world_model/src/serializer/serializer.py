from abc import ABC, abstractmethod


class ISerializer(ABC):
    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def load_from_file(self):
        pass


class JSONSerializer(ABC):
    # TODO: save_to_file
    def save_to_file(self):
        pass

    # TODO: load_from_file
    def load_from_file(self):
        pass
