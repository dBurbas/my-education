class AnimalWorldError(Exception):
    """Basic exception of the project"""

    pass


class EcosystemError(AnimalWorldError):
    """Ecosystem errors"""

    pass


class OrganismException(EcosystemError):
    "Organism errors"

    pass


class OrganismNotFoundError(OrganismException):
    def __init__(self, organism_id: int):
        self.organism_id = organism_id
        super().__init__(f"Organism with id={organism_id} not found")


class OrganismAlreadyDeadError(OrganismException):
    def __init__(self, organism_id: int):
        self.organism_id = organism_id
        super().__init__(f"Organism id={organism_id} is already dead")


class OrganismAlreadyExistsError(OrganismException):
    def __init__(self, organism_id: int):
        self.organism_id = organism_id
        super().__init__(f"Organism id={organism_id} already exists")


class GrowthValueError(OrganismException):
    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Growth value({value}) is not correct (expected int >= 0)")


class EnergyValueError(OrganismException):
    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Energy value({value}) is not correct (expected int >= 0)")


class HealthValueError(OrganismException):
    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Health value({value}) is not correct (expected int >= 0)")


class FoodChainError(EcosystemError):
    """Food chain errors"""

    pass


class FoodRuleNotFoundError(FoodChainError):
    def __init__(self, predator: type, prey: type):
        super().__init__(f"No rule: {predator.__name__} → {prey.__name__}")


class FoodRuleAlreadyExistsError(FoodChainError):
    def __init__(self, predator: type, prey: type):
        super().__init__(f"Rule already exists: {predator.__name__} → {prey.__name__}")


class CLIError(AnimalWorldError):
    """User input errors"""

    pass


class InvalidInputError(CLIError):
    def __init__(self, value: str, expected: str):
        super().__init__(f"Invalid input '{value}'. Expected: {expected}")
