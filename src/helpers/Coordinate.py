import math

from helpers.Direction import Direction


class Coordinate:
    """
    Class representing a coordinate.
    """

    def __init__(self, x: int, y: int):
        """
        Constructs a new coordinate object.
        :param x: the x coordinate
        :param y: the y coordinate
        """

        self.x: int = x
        self.y: int = y

    def add_coordinate(self, other):
        """
        Add a coordinate to this coordinate
        :param other: the other coordinate to be added
        :return: the result coordinate (a new instance)
        """

        return Coordinate(self.x + other.x, self.y + other.y)

    def add_direction(self, direction):
        """
        Move in a direction from this coordinate
        :param direction: of unit move
        :return: the new coordinate
        """
        return self.add_coordinate(self.dir_to_coordinate_delta(direction))

    def subtract_coordinate(self, other):
        """
        Subtract a coordinate from the current coordinate

        :param other: the to be subtracted coordinate
        :return: the new coordinate
        """
        return Coordinate(self.x - other.x, self.y - other.y)

    def subtract_direction(self, direction):
        """
        Move in an inverted direction from this coordinate

        :param direction: of unit move
        :return: the new coordinate
        """

        return self.subtract_coordinate(self.dir_to_coordinate_delta(direction))

    def __str__(self):
        """
        String representation of coordinate
        :return: String representation of coordinate
        """

        return str(self.x) + ", " + str(self.y)

    def __eq__(self, other):
        """
        Equals method for Coordinate.

        :param other: Other Coordinate to check
        :return: boolean (whether they're equal)
        """

        return self.x == other.x and self.y == other.y

    def x_between(self, low, up):
        """
        Check whether a point x lies within the range [low,up)

        :param low: lower bound
        :param up: upper bound (non-inclusive)
        :return: boolean (whether point lies between two coordinates)
        """

        return low <= self.x < up

    def y_between(self, low, up):
        """
        Check whether a point lies between a y range with [low,up)

        :param low: lower bound
        :param up: upper bound (non-inclusive)
        :return: boolean (whether point lies between two coordinates)
        """
        return low <= self.y < up

    def get_x(self):
        """
        :return: the x position
        """

        return self.x

    def get_y(self):
        """
        :return: the y position
        """

        return self.y

    def dir_to_coordinate_delta(self, direction):
        """
        Get vector (coordinate) of a certain direction.

        :param direction:
        :return:
        """

        # All directions in a vector
        # Creates a map with a direction linked to its (direction) vector.
        vector = {Direction.right: Coordinate(1, 0), Direction.left: Coordinate(-1, 0),
                  Direction.up: Coordinate(0, -1), Direction.down: Coordinate(0, 1),
                  Direction.up_right: Coordinate(1, -1), Direction.up_left: Coordinate(-1, -1),
                  Direction.down_right: Coordinate(1, 1), Direction.down_left: Coordinate(-1, 1)}
        return vector[direction]

    def move_in_direction(self, angle, distance):
        """
        Move in a direction from this coordinate

        :param angle: angle of movement in radians
        :param distance: distance of movement
        :return: the new coordinate
        """

        dx = distance * math.cos(angle)
        dy = distance * math.sin(angle)

        return Coordinate(self.x + dx, self.y + dy)
