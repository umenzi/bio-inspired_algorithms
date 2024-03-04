from Helper.Direction import Direction


class Route:
    """
    Class representing a route.
    """

    def __init__(self, start):
        """
        Route takes a starting coordinate to initialize.

        :param start: the starting coordinate.
        """

        self.route = []
        self.start = start

    def add(self, direction):
        """
        After taking a step we add the direction we moved in.

        :param direction: the direction we moved in.
        """

        self.route.append(direction)
        return

    def size(self):
        """
        Returns the length of the route

        :return: length of the route
        """

        return len(self.route)

    def get_route(self):
        """
        Getter for the list of directions.

        :return: list of directions
        """

        return self.route

    def get_start(self):
        """
        Getter for the starting coordinate.

        :return: the starting coordinate
        """

        return self.start

    def shorter_than(self, other):
        """
        Function that checks whether a route is smaller than another route.

        :param other: other the other route
        :return: whether the route is shorter
        """

        return self.size() < other.size()

    def remove_last(self):
        """
        Take a step back in the route and return the last direction.

        :return: the last direction
        """

        return self.route.pop()

    def __str__(self):
        """
        Build a string representing the route as the format specified in the manual.

        :return: string with the specified format of a route
        """

        string = ""
        for direction in self.route:
            string += str(Direction.dir_to_int(direction))
            string += ";\n"
        return string

    def __eq__(self, other):
        """
        Equals method for route

        :param other: the other route
        :return: whether they are equal
        """

        return self.start == other.start and self.route == other.route

    def write_to_file(self, file_path):
        """
        Method that implements the specified format for writing a route to a file.

        :param file_path: path to route file.
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
