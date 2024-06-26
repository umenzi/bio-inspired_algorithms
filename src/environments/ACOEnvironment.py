from environments.Environment import Environment

from helpers.Coordinate import Coordinate
from helpers.Path import Path
from helpers.SurroundingPheromone import SurroundingPheromone


class ACOEnvironment(Environment):
    """
    Class that holds all the environment data. This means the pheromones, the open and blocked tiles in the system as
    well as the starting and end coordinates.
    """

    def __init__(self, width: int, height: int, obstacles=None, start=None, end=None):
        super().__init__(width, height, obstacles, start, end)

        # Specific to ACO, we use pheromones to guide the ants.
        self.pheromones = None
        self.initialize_pheromones()

    def initialize_pheromones(self):
        """
        Initialize pheromones to a start value.
        """

        self.pheromones = [[1 / (self.width * self.height) for _ in range(self.height)] for _ in range(self.width)]

        for i in range(self.width):
            for j in range(self.height):
                if self.distance_to_closest_obstacle(Coordinate(i, j)) < 0:
                    self.pheromones[i][j] = 0

    def reset(self):
        self.initialize_pheromones()

    def add_pheromone_path(self, path: Path, q: int):
        """
        Update the pheromones along a certain path according to a certain Q.

        :param path: The path of the ant
        :param q: Normalization factor for the amount of dropped pheromone
        :return:
        """
        amount = 0

        if path.size() != 0:
            amount = q / path.size()

        for coordinate in path.get_path():
            self.pheromones[coordinate.x][coordinate.y] += amount

    def add_pheromone_paths(self, paths, q: int):
        """
        Update pheromones for a list of paths

        :param paths: A list of paths
        :param q: Normalization factor for amount of dropped pheromone
        :return:
        """

        for path in paths:
            self.add_pheromone_path(path, q)

    def evaporate(self, rho: float):
        """
        Evaporate pheromone

        :param rho: evaporation factor
        """

        for i in range(self.width):
            for j in range(self.height):
                self.pheromones[i][j] *= (1 - rho)

    def get_surrounding_pheromone(self, position: Coordinate, step_size: int = 1):
        """
        Returns the number of pheromones on the neighbouring positions (N/S/E/W).

        :param step_size: How many cells do we move in each direction.
        :param position: The position to check the neighbours of.
        :return: The pheromones of the neighbouring positions.
        """

        up = self.get_pheromone(Coordinate(position.x, position.y + step_size))
        up_right = self.get_pheromone(Coordinate(position.x + step_size, position.y + step_size))
        right = self.get_pheromone(Coordinate(position.x + step_size, position.y))
        down_right = self.get_pheromone(Coordinate(position.x + step_size, position.y - step_size))
        down = self.get_pheromone(Coordinate(position.x, position.y - step_size))
        down_left = self.get_pheromone(Coordinate(position.x - step_size, position.y - step_size))
        left = self.get_pheromone(Coordinate(position.x - step_size, position.y))
        up_left = self.get_pheromone(Coordinate(position.x - step_size, position.y + step_size))

        return SurroundingPheromone(up, up_right, right, down_right, down, down_left, left, up_left)

    def get_pheromone(self, pos: Coordinate):
        """
        Pheromone getter for a specific position. If the position is not in bounds, returns 0

        :param pos: Position coordinate
        :return: pheromone at point
        """

        if self.distance_to_closest_obstacle(pos) < 0:
            return 0
        return self.pheromones[pos.x][pos.y]

    @staticmethod
    def create_new_environment(width: int, height: int, obstacles=None,
                               start_pos: Coordinate = None, end_pos: Coordinate = None):
        """
        :return: a new ACO environment with the given parameters.
        """
        environment: Environment = Environment.create_environment(width, height, obstacles,
                                                                  start_pos, end_pos)

        return ACOEnvironment(environment.width, environment.height, environment.obstacles,
                              environment.start, environment.end)

    @staticmethod
    def create_from_environment(environment: Environment):
        """
        :return: a new ACO environment from the given environment.
        """
        return ACOEnvironment(environment.width, environment.height, environment.obstacles,
                              environment.start, environment.end)
