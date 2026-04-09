from core.organisms import Animal, Plant
from core.commands import SoundCommand


class CustomPlant(Plant):
    def __init__(self, *, photosynthesis_rate: float = 1.0, **kwargs):
        super().__init__(photosynthesis_rate=photosynthesis_rate, **kwargs)


class Grass(Plant):
    """Concrete plant species: Grass.

    :param photosynthesis_rate: Rate of photosynthesis. Defaults to 1.5.
    :type photosynthesis_rate: float
    """

    def __init__(self, *, photosynthesis_rate: float = 1.5, **kwargs):
        super().__init__(photosynthesis_rate=photosynthesis_rate, **kwargs)


class CustomAnimal(Animal):
    EDITABLE_TRAITS = {
        **Animal.EDITABLE_TRAITS,
        "sound": (str, None, None),
    }

    def __init__(
        self,
        *,
        hunger_rate: float = 1.0,
        vision_radius: float = 10.0,
        speed: float = 2.0,
        sound: str = "hrr...",
        **kwargs,
    ):
        self._sound = sound
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> SoundCommand:
        """Return a :class:`~commands.SoundCommand` with the custom sound.

        :return: Sound command with sound ``"custom sound"``.
        :rtype: SoundCommand
        """
        return SoundCommand(sound_maker=self, sound=self._sound)

    def clone(self, **kwargs) -> "CustomAnimal":
        kwargs.setdefault("sound", self._sound)
        return super().clone(**kwargs)


class Wolf(Animal):
    """Concrete animal species: Wolf.

    Apex predator with high vision radius and speed.

    :param hunger_rate: Hunger rate multiplier. Defaults to 1.5.
    :type hunger_rate: float
    :param vision_radius: Detection radius in habitat units. Defaults to 10.0.
    :type vision_radius: float
    :param speed: Maximum movement per tick. Defaults to 1.0.
    :type speed: float
    """

    def __init__(
        self,
        *,
        hunger_rate: float = 1.5,
        vision_radius: float = 15.0,
        speed: float = 2.0,
        **kwargs,
    ):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        """Return a :class:`~commands.SoundCommand` with the wolf's howl.

        :return: Sound command with sound ``"Awoooooof"``.
        :rtype: SoundCommand
        """
        return SoundCommand(sound_maker=self, sound="Awoooooof")


class Rabbit(Animal):
    """Concrete animal species: Rabbit.

    Herbivore with moderate vision and speed.

    :param hunger_rate: Hunger rate multiplier. Defaults to 1.0.
    :type hunger_rate: float
    :param vision_radius: Detection radius in habitat units. Defaults to 10.0.
    :type vision_radius: float
    :param speed: Maximum movement per tick. Defaults to 2.0.
    :type speed: float
    """

    def __init__(
        self,
        *,
        hunger_rate: float = 1.0,
        vision_radius: float = 15.0,
        speed: float = 2.0,
        **kwargs,
    ):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        """Return a :class:`~commands.SoundCommand` with the rabbit's sound.

        :return: Sound command with sound ``"Chump-chum"``.
        :rtype: SoundCommand
        """
        return SoundCommand(sound_maker=self, sound="Chump-chum")


class Fox(Animal):
    """Concrete animal species: Fox.

    Wide vision radius and above-average speed.

    :param hunger_rate: Hunger rate multiplier. Defaults to 1.0.
    :type hunger_rate: float
    :param vision_radius: Detection radius in habitat units. Defaults to 7.0.
    :type vision_radius: float
    :param speed: Maximum movement per tick. Defaults to 1.1.
    :type speed: float
    """

    def __init__(
        self,
        *,
        hunger_rate: float = 1.0,
        vision_radius: float = 12.0,
        speed: float = 2.5,
        **kwargs,
    ):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        """Return a :class:`~commands.SoundCommand` with the fox's sound.

        :return: Sound command with sound ``"What does the fox say"``.
        :rtype: SoundCommand
        """
        return SoundCommand(sound_maker=self, sound="What does the fox say")
