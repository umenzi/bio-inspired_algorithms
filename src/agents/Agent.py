from helpers.Coordinate import Coordinate
from helpers.PathSpecification import PathSpecification


class Agent:
    """
    Simple agent class, from where all the specific agents are implemented.
    """

    def __init__(self, environment, path_specification: PathSpecification, step_size: int = 1):
        """
        Constructor for the agent taking an environments and PathSpecification.

        :param environment: environments the ant will be running in.
        :param path_specification: The path specification consists of a start coordinate and an end coordinate.
        """

        self.environment = environment
        self.start: Coordinate = path_specification.get_start()
        self.end: Coordinate = path_specification.get_end()
        self.current_position: Coordinate = self.start
        self.step_size = step_size

    def position_out_of_bounds(self, pos: Coordinate, obstacle_distance: int = 0):
        """
        Check if within bounds OR colliding with an obstacle
        :param obstacle_distance: the required minimum distance to an obstacle
        :param pos: the position to check
        :return: True if out of bounds or colliding with an obstacle, False otherwise
        """

        x_out: bool = not (0 <= pos.x <= self.environment.width - 1)
        y_out: bool = not (0 <= pos.y <= self.environment.height - 1)
        obs: bool = self.environment.distance_to_closest_obstacle(pos) < obstacle_distance

        return x_out or y_out or obs
