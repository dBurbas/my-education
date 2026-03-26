from dataclasses import dataclass


@dataclass
class Position:
    """Position class for entities positions"""

    x: float
    y: float

    def distance_to(self, other: "Position") -> float:
        """Calculate the distance to another position using the Euclidean distance formula.
        Args:
            other (Position): The other position to which the distance is calculated.
        Returns:
            float: The distance to the other position."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
