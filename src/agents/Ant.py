import random

from agents.Agent import Agent
from environments.ACOEnvironment import ACOEnvironment
from helpers.Direction import Direction
from helpers.PathSpecification import PathSpecification
from helpers.Route import Route
import numpy as np


class Ant(Agent):
    """
    agents representing the ant functionality
    """

    def __init__(self, environment: ACOEnvironment, path_specification: PathSpecification,
                 convergence_iter: int, trail: float):
        super().__init__(environment, path_specification)

        self.rand = random
        self.convergence_iter = convergence_iter
        self.trail = trail

    def find_route(self):
        """
        Method that performs a single run through the environment by the ant.

        :return: The route the ant found through the environment.
        """

        # We start from the starting route
        route = Route(self.start)

        # By marking visited cells, in the environment and setting their pheromone level to 0, upcoming agents will
        # never choose said cells as a path to explore. This allows to avoid infinite loops where agents go over a
        # path infinite times, ending up in positions they have already visited
        visited = [self.start]

        # Improvement: the ants have memory, which allow them to know which were decision points in their so-far
        # explored path This way, we avoid dead ends, and the ants can go back to the previous decision point
        stack = []

        # Until we reach the end
        while self.current_position != self.end:
            # We get the total surrounding pheromone at the current position
            self.convergence_iter -= 1

            if self.convergence_iter == 0:
                return None

            surrounding_pheromone = self.environment.get_surrounding_pheromone(self.current_position)
            tot_pheromones = surrounding_pheromone.get_total_surrounding_pheromone()

            # Cumulative probabilities
            # Here probability = p^k_{ij}(t), where \eta_{ij}=1 (as the next direction is always one step away).
            probabilities = [0.0 for _ in range(4)]

            for i in range(4):
                if not self.current_position.add_direction(Direction(i)) in visited:
                    # Since distance = 1 always, no need for visibility parameter
                    probabilities[i] = surrounding_pheromone.get(Direction(i)) ** self.trail
                else:
                    tot_pheromones -= surrounding_pheromone.get(Direction(i))

            total = sum(probabilities)

            if tot_pheromones == 0 or total == 0:
                if len(stack) > 0:
                    self.current_position, route_length = stack.pop()
                    while route.size() > route_length:
                        route.remove_last()
                    continue
                else:
                    return None

            if len(probabilities) - probabilities.count(0) >= 2:
                stack.append((self.current_position, route.size()))

            for i in range(len(probabilities)):
                probabilities[i] /= total

            # Get index of selected direction following probability distribution
            choice = np.random.choice(range(len(probabilities)), p=probabilities)
            self.current_position = self.current_position.add_direction(Direction(choice))
            route.add(Direction(choice))

            visited.append(self.current_position)

        return route
