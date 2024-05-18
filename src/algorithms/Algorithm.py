from environments.Environment import Environment
from helpers.Path import Path
from helpers.PathSpecification import PathSpecification


class Algorithm:
    """
    An abstract class for all algorithms to inherit from.
    """

    def __init__(self, environment: Environment, step_size: int, obstacle_distance: int = 0):
        self.environment = environment
        self.step_size = step_size
        self.obstacle_distance = obstacle_distance

    def run(self, path_specification: PathSpecification, print_progress: bool = True) -> (Path, list):
        """
        The algorithm to find the shortest path across generations.

        :param path_specification: The start and end coordinates of the path
        :param print_progress: Whether we print the result of each generation

        :return: The best path found and a list of checkpoints
        """

        raise NotImplementedError
