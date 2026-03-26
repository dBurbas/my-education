from enum import Enum, auto


# TODO: доработать все docstring
class EcosystemStatus(Enum):
    STABLE = "stable"
    GROWTH = "growth"
    STRESS_LOW = "stress_low"
    STRESS_HIGH = "stress_high"
    COLLAPSE = "collapse"


class EventType(Enum):
    REPRODUCTION_EVENT = auto()
    DIE_EVENT = auto()
    EAT_EVENT = auto()
    MOVE_EVENT = auto()
    REST_EVENT = auto()
    SOUND_EVENT = auto()
    PHOTOSYNTHESIS_EVENT = auto()
