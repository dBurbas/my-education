from enum import Enum, auto


class EcosystemStatus(Enum):
    STABLE = "stable"
    GROWTH = "growth"
    STRESS_LOW = "stress_low"
    STRESS_HIGH = "stress_high"
    COLLAPSE = "collapse"


class AnimalStatus(Enum):
    IDLE = "idle"
    FEEDING = "feeding"
    MOVING = "moving"
    RESTING = "resting"
    HUNTING = "hunting"
    ESCAPING = "escaping"
    REPRODUCING = "reproducing"
    DYING = "dying"


class EventType(Enum):
    DIE_EVENT = auto()
    EAT_EVENT = auto()
    SOUND_EVENT = auto()
    PHOTOSYNTHESIS_EVENT = auto()
