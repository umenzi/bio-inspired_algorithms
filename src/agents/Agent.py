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
        :param path_specification: The path specification consisting of a start coordinate and an end coordinate.
        """
        self.environment = environment
        self.start: Coordinate = path_specification.get_start()
        self.end: Coordinate = path_specification.get_end()
        self.current_position: Coordinate = self.start
        self.step_size = step_size
