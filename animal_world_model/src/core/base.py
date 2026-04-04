from dataclasses import dataclass


@dataclass
class Position:
    """Position class for entities positions"""

    x: float
    y: float

    def distance_to(self, other: "Position") -> float:
        """Calculate the distance to another position using the Euclidean distance formula.
        (preferred for getting exact distance)

        :param: other: The other position to which the distance is calculated.
        :type: Position
        :return: The distance to the other position.
        :rtype: float"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def distance_squared_to(self, other: "Position") -> float:
        """Optimized calculation the square distance to another position
        using the Euclidean distance formula.(preferred for just checking closest)

        :param: other: The other position to which the distance is calculated.
        :type: Position
        :return: The squared distance to the other position.
        :rtype: float"""
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2
