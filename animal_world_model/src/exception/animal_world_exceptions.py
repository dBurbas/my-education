class AnimalWorldError(Exception):
    """Base exception for the project"""

    pass


class EcosystemError(AnimalWorldError):
    """Base exception for ecosystem level errors."""

    pass


class HabitatMapValuesError(AnimalWorldError):
    """Exception for wrong habitat map values"""

    def __init__(self, x_value: float, y_value: float):
        self.x_value = x_value
        self.y_value = y_value
        super().__init__(
            f"Habitat map values are incorrect ({x_value},{y_value}). Expected positive float values like (10.0 10.0)"
        )


class OrganismException(EcosystemError):
    """Base exception for organism-related errors."""

    pass


class OrganismNotFoundError(OrganismException):
    """Raised when an organism with the given ID does not exist in the ecosystem.

    :param organism_id: The ID that was not found.
    :type organism_id: int
    """

    def __init__(self, organism_id: int):
        self.organism_id = organism_id
        super().__init__(f"Organism with id={organism_id} not found")


class OrganismAlreadyDeadError(OrganismException):
    """Raised when an operation is attempted on an organism that is already dead.

    :param organism_id: The ID of the dead organism.
    :type organism_id: int
    """

    def __init__(self, organism_id: int):
        self.organism_id = organism_id
        super().__init__(f"Organism id={organism_id} is already dead")


class OrganismAlreadyExistsError(OrganismException):
    """Raised when adding an organism whose ID already exists in the ecosystem.

    :param organism_id: The duplicate ID.
    :type organism_id: int
    """

    def __init__(self, organism_id: int):
        self.organism_id = organism_id
        super().__init__(f"Organism id={organism_id} already exists")


class GrowthValueError(OrganismException):
    """Raised when a negative or otherwise invalid growth value is provided.

    :param value: The invalid value that was passed.
    :type value: int
    """

    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Growth value({value}) is not correct (expected int >= 0)")


class EnergyValueError(OrganismException):
    """Raised when a negative or otherwise invalid energy value is provided.

    :param value: The invalid value that was passed.
    :type value: int
    """

    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Energy value({value}) is not correct (expected int >= 0)")


class HealthValueError(OrganismException):
    """Raised when a negative or otherwise invalid health value is provided.

    :param value: The invalid value that was passed.
    :type value: int
    """

    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Health value({value}) is not correct (expected int >= 0)")


class SizeValueError(OrganismException):
    """Raised when a negative or otherwise invalid size value is provided.

    :param value: The invalid value that was passed.
    :type value: int
    """

    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Size value({value}) is not correct (expected int > 0)")


class AgeValueError(OrganismException):
    """Raised when a negative or otherwise invalid age value is provided.

    :param value: The invalid value that was passed.
    :type value: int
    """

    def __init__(self, value: int):
        self.value = value
        super().__init__(f"Age value({value}) is not correct (expected int >= 0)")


class GrowRateValueError(OrganismException):
    """Raised when a negative or otherwise invalid grow rate value is provided.

    :param value: The invalid value that was passed.
    :type value: int
    """

    def __init__(self, value: int):
        self.value = value
        super().__init__(
            f"Grow rate value({value}) is not correct (expected float >= 1.0)"
        )


class AnimalWorldValueError(AnimalWorldError):
    """Raised when an invalid value is provided in any part of animal world system.

    :param value: The invalid value that was passed.
    """

    def __init__(self, value, expected):
        self.value = value
        super().__init__(f"Invalid value({value}). Expected: {expected}")


class FoodChainError(EcosystemError):
    """Base exception for food-chain-related errors."""

    pass


class FoodRuleNotFoundError(FoodChainError):
    """Raised when attempting to remove a diet rule that does not exist.

    :param predator: The predator species type.
    :type predator: type
    :param prey: The prey species type.
    :type prey: type
    """

    def __init__(self, predator: type, prey: type):
        super().__init__(f"No rule: {predator.__name__} -> {prey.__name__}")


class FoodRuleAlreadyExistsError(FoodChainError):
    """Raised when attempting to add a diet rule that already exists.

    :param predator: The predator species type.
    :type predator: type
    :param prey: The prey species type.
    :type prey: type
    """

    def __init__(self, predator: type, prey: type):
        super().__init__(f"Rule already exists: {predator.__name__} -> {prey.__name__}")


class UnknownSpeciesError(AnimalWorldError):
    """Raised when a species name string does not match any registered type.

    :param species: The unrecognized species name.
    :type species: str
    """

    def __init__(self, species: str):
        super().__init__(f"Unknown species type: {species}")


class CLIError(AnimalWorldError):
    """Base exception for user-input errors in the CLI layer."""

    pass


# ? is needed
class InvalidInputError(CLIError):
    """Raised when CLI input does not match the expected format or range.

    :param value: The value the user provided.
    :type value: str
    :param expected: Description of the expected input.
    :type expected: str
    """

    def __init__(self, value: str, expected: str):
        super().__init__(f"Invalid input '{value}'. Expected: {expected}")
