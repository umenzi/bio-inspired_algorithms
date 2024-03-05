from Board.Board import Board
from Helper.Coordinate import Coordinate
from Helper.SurroundingPheromone import SurroundingPheromone
from Helper.Direction import Direction


class ACOBoard(Board):
    """
    Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
    well as the starting and end coordinates.
    """

    def __init__(self, walls, width, height):
        super().__init__(width, height, walls)

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
                if self.walls[i][j] == 0:
                    self.pheromones[i][j] = 0

    def reset(self):
        self.initialize_pheromones()

    def add_pheromone_route(self, route, q):
        """
        Update the pheromones along a certain route according to a certain Q.

        :param route: The route of the ants
        :param q: Normalization factor for amount of dropped pheromone
        :return:
        """
        amount = 0
        if route.size() != 0:
            amount = q / route.size()
        cur = route.get_start()
        self.pheromones[cur.x][cur.y] += amount
        for direction in route.get_route():
            cur = cur.add_direction(Direction(direction))
            self.pheromones[cur.x][cur.y] += amount

    def add_pheromone_routes(self, routes, q):
        """
        Update pheromones for a list of routes
        :param routes: A list of routes
        :param q: Normalization factor for amount of dropped pheromone
        :return:
        """
        for r in routes:
            self.add_pheromone_route(r, q)

    def evaporate(self, rho):
        """
        Evaporate pheromone
        :param rho: evaporation factor
        :return:
        """
        for i in range(self.width):
            for j in range(self.height):
                self.pheromones[i][j] *= (1 - rho)

    def get_surrounding_pheromone(self, position):
        """
        Returns the amount of pheromones on the neighbouring positions (N/S/E/W).
        :param position: The position to check the neighbours of.
        :return: The pheromones of the neighbouring positions.
        """
        north = self.get_pheromone(Coordinate(position.x, position.y - 1))
        south = self.get_pheromone(Coordinate(position.x, position.y + 1))
        east = self.get_pheromone(Coordinate(position.x + 1, position.y))
        west = self.get_pheromone(Coordinate(position.x - 1, position.y))

        return SurroundingPheromone(north, east, south, west)

    def get_pheromone(self, pos):
        """
        Pheromone getter for a specific position. If the position is not in bounds returns 0
        :param pos: Position coordinate
        :return: pheromone at point
        """
        if not self.in_bounds(pos):
            return 0
        return self.pheromones[pos.x][pos.y]

    @staticmethod
    def create_maze(file_path):
        maze = Board.create_maze(file_path)

        return ACOBoard(maze.walls, maze.width, maze.height)
