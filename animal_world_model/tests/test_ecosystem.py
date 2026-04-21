"""Tests for FoodChain, Habitat, Ecosystem"""

import pytest
from core.base import Position
from core.species import Wolf, Rabbit, Fox, Grass
from core.ecosystem import FoodChain, Habitat
from exception.animal_world_exceptions import (
    FoodRuleAlreadyExistsError,
    FoodRuleNotFoundError,
    HabitatMapValuesError,
    OrganismAlreadyExistsError,
    OrganismAlreadyDeadError,
    OrganismNotFoundError,
)


# ── FoodChain ────────────────────────────────────────────────────────────────


class TestFoodChain:
    def test_can_eat_valid_rule(self, food_chain, wolf, rabbit):
        assert food_chain.can_eat(eater=wolf, eaten=rabbit) is True

    def test_cannot_eat_reversed(self, food_chain, wolf, rabbit):
        """Кролик не должен есть волка"""
        assert food_chain.can_eat(eater=rabbit, eaten=wolf) is False

    def test_cannot_eat_unknown_eater(self, food_chain, grass, rabbit):
        assert food_chain.can_eat(eater=grass, eaten=rabbit) is False

    def test_classify_producer(self, food_chain, grass):
        assert food_chain.classify_organism(grass) == "producer"

    def test_classify_herbivore(self, food_chain, rabbit):
        assert food_chain.classify_organism(rabbit) == "herbivore"

    def test_classify_predator(self, food_chain, wolf):
        assert food_chain.classify_organism(wolf) == "predator"

    def test_add_new_rule(self, food_chain):
        food_chain.add_rule(eater_type=Grass, eaten_type=Rabbit)
        g = Grass(
            organism_id=99, name="g", position=Position(1, 1), photosynthesis_rate=1.0
        )
        r = Rabbit(
            organism_id=98,
            name="r",
            position=Position(2, 2),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=1.0,
        )
        assert food_chain.can_eat(eater=g, eaten=r) is True

    def test_add_duplicate_rule_raises(self, food_chain):
        with pytest.raises(FoodRuleAlreadyExistsError):
            food_chain.add_rule(eater_type=Wolf, eaten_type=Rabbit)

    def test_remove_rule(self, food_chain):
        food_chain.remove_rule(eater_type=Wolf, eaten_type=Rabbit)
        w = Wolf(
            organism_id=99,
            name="w",
            position=Position(1, 1),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=1.0,
        )
        r = Rabbit(
            organism_id=98,
            name="r",
            position=Position(2, 2),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=1.0,
        )
        assert food_chain.can_eat(eater=w, eaten=r) is False

    def test_remove_nonexistent_rule_raises(self, food_chain):
        with pytest.raises(FoodRuleNotFoundError):
            food_chain.remove_rule(eater_type=Grass, eaten_type=Wolf)

    def test_get_diet_returns_prey_list(self, food_chain):
        diet = food_chain.get_diet(Wolf)
        assert Rabbit in diet

    def test_get_diet_unknown_species_returns_empty(self, food_chain):
        assert food_chain.get_diet(Grass) == []


# ── Habitat ──────────────────────────────────────────────────────────────────


class TestHabitat:
    def test_valid_habitat_creation(self):
        h = Habitat(map=(50.0, 50.0))
        assert h.max_x == 50.0
        assert h.max_y == 50.0

    def test_zero_width_raises(self):
        with pytest.raises(HabitatMapValuesError):
            Habitat(map=(0.0, 10.0))

    def test_negative_height_raises(self):
        with pytest.raises(HabitatMapValuesError):
            Habitat(map=(10.0, -5.0))

    def test_clamp_within_bounds_unchanged(self, habitat):
        pos = Position(50.0, 50.0)
        clamped = habitat.clamp_position(pos)
        assert clamped.x == 50.0
        assert clamped.y == 50.0

    def test_clamp_over_max(self, habitat):
        pos = Position(9999.0, 9999.0)
        clamped = habitat.clamp_position(pos)
        assert clamped.x == habitat.max_x
        assert clamped.y == habitat.max_y

    def test_clamp_below_zero(self, habitat):
        pos = Position(-10.0, -5.0)
        clamped = habitat.clamp_position(pos)
        assert clamped.x == 0.0
        assert clamped.y == 0.0


# ── Ecosystem ─────────────────────────────────────────────────────────────────


class TestEcosystem:
    def test_initial_organism_count(self, ecosystem):
        assert len(ecosystem.organisms) == 3

    def test_add_organism(self, ecosystem):
        new_fox = Fox(
            organism_id=50,
            name="NewFox",
            position=Position(20.0, 20.0),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=1.0,
        )
        ecosystem.add_organism(new_fox)
        assert len(ecosystem.organisms) == 4

    def test_add_duplicate_id_raises(self, ecosystem):
        """wolf уже есть в ecosystem с id=1"""
        duplicate = Wolf(
            organism_id=1,
            name="Duplicate",
            position=Position(30.0, 30.0),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=1.0,
        )
        with pytest.raises(OrganismAlreadyExistsError):
            ecosystem.add_organism(duplicate)

    def test_add_dead_organism_raises(self, ecosystem):
        dead = Wolf(
            organism_id=77,
            name="Dead",
            position=Position(10.0, 10.0),
            hunger_rate=1.0,
            vision_radius=5.0,
            speed=1.0,
        )
        dead.die()
        with pytest.raises(OrganismAlreadyDeadError):
            ecosystem.add_organism(dead)

    def test_remove_organism_kills_it(self, ecosystem, wolf):
        ecosystem.remove_organism(wolf.organism_id)
        assert not wolf.is_alive()

    def test_remove_nonexistent_raises(self, ecosystem):
        with pytest.raises(OrganismNotFoundError):
            ecosystem.remove_organism(9999)

    def test_get_population_stats(self, ecosystem):
        stats = ecosystem.get_population_stats()
        assert stats.get("Wolf") == 1
        assert stats.get("Rabbit") == 1
        assert stats.get("Grass") == 1

    def test_get_organisms_in_radius_finds_neighbor(self, ecosystem, wolf, rabbit):
        """Wolf на (5,5), Rabbit на (6,6) — расстояние ~1.41, радиус 10"""
        neighbors = ecosystem.get_organisms_in_radius(wolf.position, radius=10.0)
        assert rabbit in neighbors

    def test_get_organisms_in_radius_excludes_self(self, ecosystem, wolf):
        neighbors = ecosystem.get_organisms_in_radius(wolf.position, radius=100.0)
        assert wolf not in neighbors

    def test_get_organisms_in_radius_excludes_far(self, ecosystem, wolf, grass):
        """Grass на (50,50), Wolf на (5,5) — расстояние ~63, радиус 5"""
        neighbors = ecosystem.get_organisms_in_radius(wolf.position, radius=5.0)
        assert grass not in neighbors

    def test_get_eco_balance_has_expected_keys(self, ecosystem):
        balance = ecosystem.get_eco_balance()
        for key in ("producer", "herbivore", "predator", "omnivore"):
            assert key in balance

    def test_tick_does_not_crash(self, ecosystem):
        ecosystem.tick()

    def test_tick_removes_dead_organisms(self, ecosystem, wolf):
        wolf.die()
        ecosystem.tick()
        assert wolf not in ecosystem.organisms
