from environments.Environment import Environment
from helpers.Coordinate import Coordinate
from helpers.PathSpecification import PathSpecification


class Agent:
    """
    Simple agent class, from where all the specific agents are implemented.
    """

    def __init__(self, environment: Environment, path_specification: PathSpecification):
        """
        Constructor for the agent taking an environments and PathSpecification.

        :param environment: environments the ant will be running in.
        :param path_specification: The path specification consisting of a start coordinate and an end coordinate.
        """
        self.environment: Environment = environment
        self.start: Coordinate = path_specification.get_start()
        self.end: Coordinate = path_specification.get_end()
        self.current_position: Coordinate = self.start
