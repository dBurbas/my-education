from abc import ABC, abstractmethod


# TODO: Typehints
class ISaver(ABC):
    # TODO: save method
    @abstractmethod
    def save(self):
        pass
