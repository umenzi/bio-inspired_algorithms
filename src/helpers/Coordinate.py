import math

from helpers.Direction import Direction


class Coordinate:
    """
    Class representing a coordinate.
    """

    def __init__(self, x: float, y: float):
        """
        Constructs a new coordinate object.
        :param x: The x coordinate
        :param y: The y coordinate
        """

        self.x: float = x
        self.y: float = y

    def add_coordinate(self, other, step_size: float = 1):
        """
        Add a coordinate to this coordinate.

        :param step_size: How many cells to move in the direction
        :param other: The other coordinate to be added
        :return: The result coordinate (a new instance)
        """

        return Coordinate(self.x + other.x * step_size, self.y + other.y * step_size)

    def add_direction(self, direction, step_size: float = 1):
        """
        Move in a direction from this coordinate.

        :param step_size: How many cells to move in the direction
        :param direction: Of unit move
        :return: The new coordinate
        """

        return self.add_coordinate(self.dir_to_coordinate_delta(direction), step_size)

    def subtract_coordinate(self, other):
        """
        Subtract a coordinate from the current coordinate

        :param other: The to be subtracted coordinate
        :return: The new coordinate
        """

        return Coordinate(self.x - other.x, self.y - other.y)

    def subtract_direction(self, direction):
        """
        Move in an inverted direction from this coordinate

        :param direction: Of unit move
        :return: The new coordinate
        """

        return self.subtract_coordinate(self.dir_to_coordinate_delta(direction))

    def __str__(self):
        """
        String representation of coordinate.

        :return: String representation of coordinate
        """

        return str(self.x) + ", " + str(self.y)

    def __eq__(self, other):
        """
        Equals method for Coordinate.

        :param other: Other Coordinate to check
        :return: Boolean (whether they're equal)
        """

        return self.x == other.x and self.y == other.y

    def x_between(self, low, up):
        """
        Check whether a point x lies within the range [low,up)

        :param low: Lower bound
        :param up: Upper bound (non-inclusive)
        :return: Boolean (whether point lies between two coordinates)
        """

        return low <= self.x < up

    def y_between(self, low, up):
        """
        Check whether a point lies between a y range with [low,up)

        :param low: Lower bound
        :param up: Upper bound (non-inclusive)
        :return: Boolean (whether point lies between two coordinates)
        """

        return low <= self.y < up

    def get_x(self):
        """
        :return: The x position
        """

        return self.x

    def get_y(self):
        """
        :return: The y position
        """

        return self.y

    def dir_to_coordinate_delta(self, direction):
        """
        Get vector (coordinate) of a certain direction.
        """

        # All directions in a vector
        # Creates a map with a direction linked to its (direction) vector.
        vector = self.get_all_directions()

        return vector[direction]

    def get_all_directions(self):
        """
        :return: All directions: up, up_right, right, down_right, down, down_left, left, up_left.
        """

        return {Direction.up: Coordinate(0, 1), Direction.up_right: Coordinate(1, 1),
                Direction.right: Coordinate(1, 0), Direction.down_right: Coordinate(1, -1),
                Direction.down: Coordinate(0, -1), Direction.down_left: Coordinate(-1, -1),
                Direction.left: Coordinate(-1, 0), Direction.up_left: Coordinate(-1, 1)}

    def move_in_direction(self, angle, distance):
        """
        Move in a direction from this coordinate.

        :param angle: Angle of movement in radians
        :param distance: Distance of movement
        :return: The new coordinate
        """

        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)

        return Coordinate(self.x + dx, self.y + dy)

    def distance_to(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
