from helpers.Coordinate import Coordinate


class PathSpecification:
    """
    Specification of a path containing a start and end coordinate.
    """

    def __init__(self, start: Coordinate, end: Coordinate):
        """
        Constructs a new path specification.

        :param start: The starting coordinate.
        :param end: The final coordinate.
        """

        self.start: Coordinate = start
        self.end: Coordinate = end

    def get_start(self):
        """
        :return: The starting coordinate
        """

        return self.start

    def get_end(self):
        """
        :return: The final coordinate
        """

        return self.end

    def __eq__(self, other):
        """
        Equals method for PathSpecification.

        :param other: The other PathSpecification
        :return: Whether they're equal
        """

        return self.start == other.start and self.end == other.end

    def __str__(self):
        """
        String representation of path specification
        :return: The representation
        """

        return "Start: " + str(self.start) + " End: " + str(self.end)

    @staticmethod
    def read_coordinates(start_pos: (int, int), end_pos: (int, int)):
        """
        Reads the coordinates and returns a path specification.

        :param start_pos: Starting position of the agent(s)
        :param end_pos: Final position of the agent(s)
        :return: Specification of the environment.
        """

        start_coordinate = Coordinate(start_pos[0], start_pos[1])
        end_coordinate = Coordinate(end_pos[0], end_pos[1])

        return PathSpecification(start_coordinate, end_coordinate)
