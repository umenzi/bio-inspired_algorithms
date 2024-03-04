import re
import traceback
import sys
from Helper.Coordinate import Coordinate


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
    def read_coordinates(file_path):
        """
        Reads the coordinates file and returns a path specification.

        :param file_path: String of the path to the file.
        :return: Specification contained in the file.
        """

        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()

            start = re.compile("[,;]\\s*").split(lines[0])
            start_x = int(start[0])
            start_y = int(start[1])

            end = re.compile("[,;]\\s*").split(lines[1])
            end_x = int(end[0])
            end_y = int(end[1])

            start_coordinate = Coordinate(start_x, start_y)
            end_coordinate = Coordinate(end_x, end_y)
            return PathSpecification(start_coordinate, end_coordinate)
        except FileNotFoundError:
            print("Error reading coordinate file " + file_path)
            traceback.print_exc()
            sys.exit()
