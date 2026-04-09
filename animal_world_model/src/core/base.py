from dataclasses import dataclass


@dataclass
class Position:
    """Represents a 2D coordinate in the simulation space.

    :param x: Horizontal coordinate.
    :type x: float
    :param y: Vertical coordinate.
    :type y: float
    """

    x: float
    y: float

    def distance_to(self, other: "Position") -> float:
        """Calculate the Euclidean distance to another position.

        Preferred when the exact distance value is needed.

        :param other: The target position.
        :type other: Position
        :return: Euclidean distance between the two positions.
        :rtype: float
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def distance_squared_to(self, other: "Position") -> float:
        """Calculate the squared Euclidean distance to another position.

        Avoids the square root operation; preferred when only comparing distances
        (e.g. finding the closest target) rather than needing the exact value.

        :param other: The target position.
        :type other: Position
        :return: Squared Euclidean distance between the two positions.
        :rtype: float
        """
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2
