class AthleteManagerError(Exception):
    """Base exception for the project"""

    pass


class AthleteTypeError(AthleteManagerError):
    """Exception for non correct type for athlete data"""

    def __init__(self, given_type: type, expected_type: type):
        self.expected_type = expected_type
        self.given_type = given_type
        super().__init__(
            f"Некорректный тип данных спортсмена. Передан:{given_type} (ожидалось: {expected_type})."
        )
