from helpers.Coordinate import Coordinate


class Route:
    """
    Class representing a route.
    """

    def __init__(self, start: Coordinate):
        """
        Route takes a starting coordinate to initialize.

        :param start: The starting coordinate.
        """

        self.route = [start]
        self.start: Coordinate = start

    def add(self, coordinate: Coordinate):
        """
        After taking a step, we add the direction we moved in.

        :param coordinate: The coordinate we moved in.
        """

        self.route.append(coordinate)
        return

    def size(self):
        """
        Returns the length of the route

        :return: Length of the route
        """

        return len(self.route)

    def get_route(self):
        """
        Getter for the list of directions.

        :return: List of directions
        """

        return self.route

    def get_start(self):
        """
        Getter for the starting coordinate.

        :return: The starting coordinate
        """

        return self.start

    def shorter_than(self, other):
        """
        Function that checks whether a route is smaller than another route.

        :param other: Other the other route
        :return: Whether the route is shorter
        """

        return self.size() < other.size()

    def remove_last(self):
        """
        Take a step back in the route and return the last direction.

        :return: The last direction
        """

        return self.route.pop()

    def __str__(self):
        """
        Build a string representing the route as the format specified in the manual.

        :return: String with the specified format of a route
        """

        string = ""

        for coordinate in self.route:
            string += str(coordinate)
            string += ";\n"

        return string

    def __eq__(self, other):
        """
        Equals method for route

        :param other: The other route
        :return: Whether they are equal
        """

        return self.start == other.start and self.route == other.route

    def write_to_file(self, file_path):
        """
        Method that implements the specified format for writing a route to a file.

        :param file_path: Path to route file.
        :raises: IOError if the file path is invalid.
        """

        f = open(file_path, "w")
        string = ""
        string += str(len(self.route))
        string += ";\n"
        string += str(self.start)
        string += ";\n"
        string += str(self)
        f.write(string)
