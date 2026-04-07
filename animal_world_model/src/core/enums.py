from enum import Enum, auto


# TODO: нужен ли класс состояний экосистемы?
class EcosystemStatus(Enum):
    STABLE = "stable"
    GROWTH = "growth"
    STRESS_LOW = "stress_low"
    STRESS_HIGH = "stress_high"
    COLLAPSE = "collapse"


class EventType(Enum):
    """Enumeration of all simulation event types dispatched through EventManager.

    :cvar REPRODUCTION_EVENT: An organism has reproduced.
    :cvar DIE_EVENT: An organism has died (generic).
    :cvar DIE_EATEN_EVENT: An organism died by being eaten.
    :cvar DIE_STARVATION_EVENT: An organism died from starvation.
    :cvar DIE_OLD_EVENT: An organism died of old age.
    :cvar EAT_EVENT: An organism has consumed another.
    :cvar MOVE_EVENT: An organism has moved.
    :cvar REST_EVENT: An organism is resting.
    :cvar SOUND_EVENT: An organism produced a sound.
    :cvar PHOTOSYNTHESIS_EVENT: A plant performed photosynthesis.
    """

    REPRODUCTION_EVENT = auto()
    DIE_EVENT = auto()
    DIE_EATEN_EVENT = auto()
    DIE_STARVATION_EVENT = auto()
    DIE_OLD_EVENT = auto()
    EAT_EVENT = auto()
    MOVE_EVENT = auto()
    REST_EVENT = auto()
    SOUND_EVENT = auto()
    PHOTOSYNTHESIS_EVENT = auto()
