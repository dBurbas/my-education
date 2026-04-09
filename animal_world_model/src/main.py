from core.ecosystem import (
    Ecosystem,
    Habitat,
    FoodChain,
)

from controller.controller import SimulationController
from interface.ecosystem_cli import EcosystemCLI
from core.species import Wolf, Rabbit, Grass, Fox
from core.factory import DefaultOrganismFactory
from core.base import Position
from core.event_manager import EventManager


def main():

    em = EventManager()
    habitat = Habitat(map=(70.0, 70.0))
    factory = DefaultOrganismFactory(start_id=7)

    fc = FoodChain(
        diet_rules={Wolf: [Rabbit, Fox], Fox: [Fox], Rabbit: [Grass], Grass: []}
    )

    initial_organisms = [
        Wolf(
            organism_id=1,
            name="Wolf_1",
            position=Position(5.0, 5.0),
            hunger_rate=2.0,
            vision_radius=10.0,
            speed=3.0,
        ),
        Rabbit(
            organism_id=2,
            name="Rabbit_1",
            position=Position(5.5, 5.5),
            hunger_rate=1.0,
        ),
        Rabbit(
            organism_id=3,
            name="Rabbit_2",
            position=Position(10.0, 10.0),
            hunger_rate=1.0,
            vision_radius=15.0,
            speed=2.0,
        ),
        Rabbit(
            organism_id=3,
            name="Rabbit_3",
            position=Position(50.0, 50.0),
            hunger_rate=1.0,
            vision_radius=15.0,
            speed=5.0,
        ),
        Grass(
            organism_id=4,
            name="Grass_1",
            position=Position(50.0, 50.0),
            photosynthesis_rate=1.5,
        ),
        Grass(
            organism_id=5,
            name="Grass_2",
            position=Position(7.0, 7.0),
            photosynthesis_rate=1.5,
        ),
        Grass(
            organism_id=5,
            name="Grass_2",
            position=Position(1.0, 5.0),
            photosynthesis_rate=1.5,
        ),
        Fox(
            organism_id=6,
            name="Fox_1",
            position=Position(15.0, 7.0),
            hunger_rate=1.5,
            vision_radius=11.0,
            speed=2.5,
        ),
    ]

    eco = Ecosystem(
        event_manager=em,
        habitat=habitat,
        organisms=initial_organisms,
        food_chain=fc,
        factory=factory,
    )

    controller = SimulationController(ecosystem=eco, factory=factory, food_chain=fc)

    cli = EcosystemCLI(controller=controller)

    print("\n[Success] Ecosystem was build! Run interface...\n")
    cli.cmdloop()


if __name__ == "__main__":
    main()
