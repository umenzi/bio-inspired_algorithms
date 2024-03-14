from helpers.Coordinate import Coordinate


class PathSpecification:
    """
    Specification of a path containing a start and end coordinate.
    """

    def __init__(self, start, end):
        """
        Constructs a new path specification.

        :param start: the starting coordinate.
        :param end: the final coordinate.
        """

        self.start = start
        self.end = end

    def get_start(self):
        """
        :return: the starting coordinate
        """

        return self.start

    def get_end(self):
        """
        :return: the final coordinate
        """
        return self.end

    def __eq__(self, other):
        """
        Equals method for PathSpecification.

        :param other: the other PathSpecification
        :return: whether they're equal
        """

        return self.start == other.start and self.end == other.end

    def __str__(self):
        """
        String representation of path specification
        :return: the representation
        """

        return "Start: " + str(self.start) + " End: " + str(self.end)

    @staticmethod
    def read_coordinates(start_pos: (int, int), end_pos: (int, int)):
        """
        Reads the coordinates and returns a path specification.

        :param start_pos: starting position of the agents
        :param end_pos: final position of the agents
        :return: Specification of the environment.
        """

        start_coordinate = Coordinate(start_pos[0], start_pos[1])
        end_coordinate = Coordinate(end_pos[0], end_pos[1])
        return PathSpecification(start_coordinate, end_coordinate)
