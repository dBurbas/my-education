import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from core.base import Position
from core.species import Wolf, Rabbit, Fox, Grass
from core.event_manager import EventManager
from core.ecosystem import Ecosystem, Habitat, FoodChain
from core.factory import DefaultOrganismFactory


@pytest.fixture
def pos():
    return Position(5.0, 5.0)


@pytest.fixture
def event_manager():
    return EventManager()


@pytest.fixture
def habitat():
    return Habitat(map=(100.0, 100.0))


@pytest.fixture
def food_chain():
    return FoodChain(
        diet_rules={
            Wolf: [Rabbit, Fox],
            Fox: [Rabbit],
            Rabbit: [Grass],
            Grass: [],
        }
    )


@pytest.fixture
def factory():
    return DefaultOrganismFactory(start_id=100)


@pytest.fixture
def wolf(pos):
    return Wolf(
        organism_id=1,
        name="TestWolf",
        position=pos,
        hunger_rate=1.5,
        vision_radius=10.0,
        speed=2.0,
    )


@pytest.fixture
def rabbit():
    return Rabbit(
        organism_id=2,
        name="TestRabbit",
        position=Position(6.0, 6.0),
        hunger_rate=1.0,
        vision_radius=10.0,
        speed=2.0,
    )


@pytest.fixture
def grass():
    return Grass(
        organism_id=3,
        name="TestGrass",
        position=Position(50.0, 50.0),
        photosynthesis_rate=1.5,
    )


@pytest.fixture
def ecosystem(event_manager, habitat, wolf, rabbit, grass, food_chain, factory):
    return Ecosystem(
        event_manager=event_manager,
        habitat=habitat,
        organisms=[wolf, rabbit, grass],
        food_chain=food_chain,
        factory=factory,
    )
