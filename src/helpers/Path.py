from helpers.Coordinate import Coordinate


class Path:
    """
    Class representing a path.
    """

    def __init__(self, start: Coordinate):
        """
        Path takes a starting coordinate to initialize.

        :param start: The starting coordinate.
        """

        self.path = [start]
        self.start: Coordinate = start

    def add(self, coordinate: Coordinate):
        """
        After taking a step, we add the direction we moved in.

        :param coordinate: The coordinate we moved in.
        """

        self.path.append(coordinate)
        return

    def size(self):
        """
        Returns the length of the path

        :return: Length of the path
        """

        return len(self.path)

    def get_path(self):
        """
        Getter for the list of directions.

        :return: List of directions
        """

        return self.path

    def get_start(self):
        """
        Getter for the starting coordinate.

        :return: The starting coordinate
        """

        return self.start

    def shorter_than(self, other):
        """
        Function that checks whether a path is smaller than another path.

        :param other: Other the other path
        :return: Whether the path is shorter
        """

        return self.size() < other.size()

    def remove_last(self):
        """
        Take a step back in the path and return the last direction.

        :return: The last direction
        """

        return self.path.pop()

    def __str__(self):
        """
        Build a string representing the path as the format specified in the manual.

        :return: String with the specified format of a path
        """

        string = ""

        for coordinate in self.path:
            string += str(coordinate)
            string += ";\n"

        return string

    def __eq__(self, other):
        """
        Equals method for the path

        :param other: The other path
        :return: Whether they are equal
        """

        return self.start == other.start and self.path == other.path

    def write_to_file(self, file_path):
        """
        Method that implements the specified format for writing a path to a file.

        :param file_path: Path to path file.
        :raises: IOError if the file path is invalid.
        """

        f = open(file_path, "w")
        string = ""
        string += str(len(self.path))
        string += ";\n"
        string += str(self.start)
        string += ";\n"
        string += str(self)
        f.write(string)
