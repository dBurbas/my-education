from src.animal_world.core.ecosystem import (
    Ecosystem,
    Habitat,
    FoodChain,
)
from src.animal_world.serializer.serializer import JSONSaver, JSONLoader
from apps.cli.controller.controller import SimulationController
from apps.cli.interface.ecosystem_cli import EcosystemCLI
from src.animal_world.core.factory import DefaultOrganismFactory
from src.animal_world.core.event_manager import EventManager


def main():

    em = EventManager()
    habitat = Habitat(map=(70.0, 70.0))
    factory = DefaultOrganismFactory()

    fc = FoodChain(diet_rules={})

    initial_organisms = []

    eco = Ecosystem(
        event_manager=em,
        habitat=habitat,
        organisms=initial_organisms,
        food_chain=fc,
        factory=factory,
    )

    controller = SimulationController(
        ecosystem=eco,
        factory=factory,
        food_chain=fc,
        saver=JSONSaver(),
        loader=JSONLoader(factory=factory),
    )

    cli = EcosystemCLI(controller=controller)

    print("\n[Success] Ecosystem was build! Run interface...\n")
    cli.cmdloop()


if __name__ == "__main__":
    main()
