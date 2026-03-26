from core.ecosystem import (
    Ecosystem,
    EventManager,
    Habitat,
    FoodChain,
    DefaultOrganismFactory,
)
from controller.controller import SimulationController
from interface.ecosystem_cli import EcosystemCLI
from core.organisms import Wolf, Rabbit, Grass, Fox
from core.base import Position


def main():

    em = EventManager()
    habitat = Habitat(map=(20.0, 20.0))
    factory = DefaultOrganismFactory()

    # Настраиваем пищевую цепь: Волк ест Кролика, Кролик ест Траву
    fc = FoodChain(diet_rules={Wolf: [Rabbit, Fox], Fox: [Fox], Rabbit: [Grass]})

    initial_organisms = [
        Wolf(
            id=1,
            name="Wolf_1",
            position=Position(5.0, 5.0),
            hunger_rate=2.0,
            vision_radius=10.0,
            speed=3.0,
        ),
        Rabbit(
            id=2,
            name="Rabbit_1",
            position=Position(6.0, 6.0),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=2.0,
        ),
        Rabbit(
            id=3,
            name="Rabbit_2",
            position=Position(15.0, 15.0),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=2.0,
        ),
        Grass(
            id=4, name="Grass_1", position=Position(6.0, 6.0), photosynthesis_rate=1.5
        ),
        Grass(
            id=5, name="Grass_2", position=Position(7.0, 7.0), photosynthesis_rate=1.5
        ),
        Fox(
            id=6,
            name="Fox_1",
            position=Position(15.0, 7.0),
            hunger_rate=1.5,
            vision_radius=11.0,
            speed=2.5,
        ),
    ]

    eco = Ecosystem(
        some_event_manager=em,
        some_habitat=habitat,
        some_organisms=initial_organisms,
        some_food_chain=fc,
        factory=factory,
    )

    controller = SimulationController(ecosystem=eco)

    cli = EcosystemCLI(controller=controller)

    print("\n[Успех] Экосистема собрана! Запуск интерфейса...\n")
    cli.cmdloop()


if __name__ == "__main__":
    main()
