from organisms import Animal, Plant
from commands import SoundCommand


class Grass(Plant):
    def __init__(self, *, photosynthesis_rate: float = 1.0, **kwargs):
        super().__init__(photosynthesis_rate=photosynthesis_rate, **kwargs)


class Wolf(Animal):
    def __init__(
        self,
        *,
        hunger_rate: float = 1.5,
        vision_radius: float = 10.0,
        speed: float = 1.0,
        **kwargs,
    ):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        return SoundCommand(sound_maker=self, sound="Awoooooof")


class Rabbit(Animal):
    def __init__(
        self,
        *,
        hunger_rate: float = 1.0,
        vision_radius: float = 5.0,
        speed: float = 1.0,
        **kwargs,
    ):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        return SoundCommand(sound_maker=self, sound="Chump-chum")


class Fox(Animal):
    def __init__(
        self,
        *,
        hunger_rate: float = 1.0,
        vision_radius: float = 7.0,
        speed: float = 1.1,
        **kwargs,
    ):
        super().__init__(
            hunger_rate=hunger_rate, vision_radius=vision_radius, speed=speed, **kwargs
        )

    def make_sound(self) -> "SoundCommand":
        return SoundCommand(sound_maker=self, sound="What does the fox say")
