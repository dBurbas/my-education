"""Tests for DefaultOrganismFactory"""

import pytest
from core.factory import DefaultOrganismFactory
from core.species import Wolf, Rabbit, Grass
from exception.animal_world_exceptions import UnknownSpeciesError
from config import STARTER_ENERGY, STARTER_HEALTH


class TestDefaultOrganismFactory:
    def test_create_wolf_by_name(self, factory):
        org = factory.create_organism("Wolf", name="W1", x=10.0, y=10.0)
        assert isinstance(org, Wolf)
        assert org.name == "W1"

    def test_create_grass_by_name(self, factory):
        org = factory.create_organism("Grass", name="G1", x=5.0, y=5.0)
        assert isinstance(org, Grass)

    def test_create_unknown_species_raises(self, factory):
        with pytest.raises(UnknownSpeciesError):
            factory.create_organism("Dragon", name="D1", x=1.0, y=1.0)

    def test_ids_are_unique_and_incrementing(self, factory):
        a = factory.create_organism("Wolf", name="A", x=1.0, y=1.0)
        b = factory.create_organism("Rabbit", name="B", x=2.0, y=2.0)
        assert b.organism_id == a.organism_id + 1

    def test_create_offspring_same_type(self, factory, wolf):
        baby = factory.create_offspring(parent=wolf)
        assert isinstance(baby, Wolf)

    def test_create_offspring_name_contains_jr(self, factory, wolf):
        baby = factory.create_offspring(parent=wolf)
        assert "Jr." in baby.name

    def test_create_offspring_has_starter_stats(self, factory, wolf):
        baby = factory.create_offspring(parent=wolf)
        assert baby.energy == STARTER_ENERGY
        assert baby.health == STARTER_HEALTH
        assert baby.age == 0

    def test_get_available_species_contains_defaults(self, factory):
        species = factory.get_available_species()
        for name in ("Wolf", "Rabbit", "Grass", "Fox"):
            assert name in species

    def test_get_traits_returns_dict_with_energy(self, factory):
        traits = factory.get_traits("Wolf")
        assert isinstance(traits, dict)
        assert "energy" in traits

    def test_species_to_type_resolves_rabbit(self, factory):
        assert factory.species_to_type("Rabbit") is Rabbit

    def test_species_to_type_unknown_raises(self, factory):
        with pytest.raises(UnknownSpeciesError):
            factory.species_to_type("Unicorn")

    def test_get_registry_returns_copy(self, factory):
        reg = factory.get_registry()
        reg["Fake"] = object
        assert "Fake" not in factory.get_registry()
