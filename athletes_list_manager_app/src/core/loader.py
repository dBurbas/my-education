from abc import ABC, abstractmethod


# TODO: Typehints
class ILoader(ABC):
    # TODO: load method
    @abstractmethod
    def load(self):
        pass
