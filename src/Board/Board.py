import sys
import traceback


class Board:
    """
    Board Class, used by all the Bio-Inspired AI algorithms.

    Note that we may want to use specific implementations of
    the Board class for each algorithm, as some use pheromones, etc.
    """

    def __init__(self, width, height, walls):
        """
        Constructor of a maze.
        :param width: of Maze (horizontal)
        :param height: of Maze (vertical)
        :param walls: int array of tiles accessible (1) and non-accessible (0)
        """
        self.width = width
        self.height = height
        self.walls = walls

        self.start = None
        self.end = None

    def get_width(self):
        """
        Width getter
        :return: width of the maze
        """
        return self.width

    def get_height(self):
        """
        Height getter
        :return: height of the maze
        """
        return self.height

    def reset(self):
        """
        Reset the maze for a new shortest path problem.
        """
        pass

    def in_bounds(self, position):
        """
        Check whether a coordinate lies in the current maze.

        :param position: The position to be checked
        :return: Whether the position is in the current maze
        """
        return position.x_between(0, self.width) and position.y_between(0, self.height) and self.walls[position.x][
            position.y] == 1

    def __str__(self):
        """
        Representation of Maze as defined by the input file format.

        :return: String representation
        """
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.height)
        string += " \n"
        for y in range(self.height):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    @staticmethod
    def create_maze(file_path):
        """
        Method that builds a mze from a file.

        :param file_path: filePath Path to the file
        :return: A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
        """
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])

            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])

            for y in range(length):
                line = lines[y + 1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Board(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()
