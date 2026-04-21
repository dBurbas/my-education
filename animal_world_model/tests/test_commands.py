"""Tests for Command classes"""

import pytest
from core.base import Position
from core.commands import (
    EatCommand,
    RestCommand,
    ReproduceCommand,
    MoveCommand,
    SoundCommand,
)
from core.enums import EventType
from config import ENERGY_ADD, HEALTH_ADD


class TestEatCommand:
    def test_eater_gains_food_energy(self, ecosystem, wolf, rabbit):
        food_energy = rabbit.energy
        energy_before = wolf.energy
        EatCommand(eater=wolf, food=rabbit).execute(ecosystem)
        assert wolf.energy == energy_before + food_energy

    def test_food_dies_after_eating(self, ecosystem, wolf, rabbit):
        EatCommand(eater=wolf, food=rabbit).execute(ecosystem)
        assert not rabbit.is_alive()

    def test_eat_skipped_if_eater_dead(self, ecosystem, wolf, rabbit):
        wolf.die()
        health_before = rabbit.health
        EatCommand(eater=wolf, food=rabbit).execute(ecosystem)
        assert rabbit.health == health_before  # кролик не тронут

    def test_eat_skipped_if_food_dead(self, ecosystem, wolf, rabbit):
        rabbit.die()
        energy_before = wolf.energy
        EatCommand(eater=wolf, food=rabbit).execute(ecosystem)
        assert wolf.energy == energy_before  # волк ничего не получил


class TestRestCommand:
    def test_rest_restores_energy(self, ecosystem, wolf):
        wolf.lose_energy(50)
        energy_before = wolf.energy
        RestCommand(resting=wolf).execute(ecosystem)
        assert wolf.energy == energy_before + ENERGY_ADD

    def test_rest_restores_health(self, ecosystem, wolf):
        wolf.lose_health(30)
        health_before = wolf.health
        RestCommand(resting=wolf).execute(ecosystem)
        assert wolf.health == health_before + HEALTH_ADD

    def test_rest_skipped_if_dead(self, ecosystem, wolf):
        wolf.die()
        energy_snapshot = wolf.energy
        RestCommand(resting=wolf).execute(ecosystem)
        assert wolf.energy == energy_snapshot


class TestMoveCommand:
    def test_move_changes_position(self, ecosystem, wolf):
        original_pos = wolf.position
        target = Position(50.0, 50.0)
        MoveCommand(mover=wolf, target_position=target).execute(ecosystem)
        assert wolf.position != original_pos

    def test_move_costs_energy(self, ecosystem, wolf):
        energy_before = wolf.energy
        MoveCommand(mover=wolf, target_position=Position(50.0, 50.0)).execute(ecosystem)
        assert wolf.energy < energy_before

    def test_move_clamps_to_habitat_bounds(self, ecosystem, wolf):
        MoveCommand(mover=wolf, target_position=Position(9999.0, 9999.0)).execute(
            ecosystem
        )
        assert wolf.position.x <= ecosystem.habitat.max_x
        assert wolf.position.y <= ecosystem.habitat.max_y

    def test_sprint_moves_further_than_walk(self, ecosystem, pos):
        from src.core.species import Wolf

        w1 = Wolf(
            organism_id=10,
            name="W1",
            position=Position(0.0, 0.0),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=2.0,
        )
        w2 = Wolf(
            organism_id=11,
            name="W2",
            position=Position(0.0, 0.0),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=2.0,
        )
        target = Position(100.0, 0.0)
        MoveCommand(mover=w1, target_position=target, is_sprinting=False).execute(
            ecosystem
        )
        MoveCommand(mover=w2, target_position=target, is_sprinting=True).execute(
            ecosystem
        )
        assert w2.position.x > w1.position.x


class TestReproduceCommand:
    def test_reproduce_adds_offspring(self, ecosystem, wolf):
        count_before = len(ecosystem.organisms)
        wolf.gain_energy(200)
        ReproduceCommand(reproducer=wolf).execute(ecosystem)
        assert len(ecosystem.organisms) == count_before + 1

    def test_reproduce_costs_energy(self, ecosystem, wolf):
        wolf.gain_energy(200)
        energy_before = wolf.energy
        ReproduceCommand(reproducer=wolf).execute(ecosystem)
        assert wolf.energy < energy_before

    def test_reproduce_skipped_if_low_energy(self, ecosystem, wolf):
        wolf.lose_energy(wolf.energy - 1)
        count_before = len(ecosystem.organisms)
        ReproduceCommand(reproducer=wolf).execute(ecosystem)
        assert len(ecosystem.organisms) == count_before
