import random

from Agent.Agent import Agent
from Helper.Direction import Direction
from Helper.Route import Route
import numpy as np


class Ant(Agent):
    """
    Agent representing the ant functionality
    """

    def __init__(self, maze, path_specification, convergence_iter, trail):
        super().__init__(maze, path_specification)
        self.rand = random
        self.convergence_iter = convergence_iter
        self.trail = trail

    def find_route(self):
        """
        Method that performs a single run through the maze by the ant.
        :return: The route the ant found through the maze.
        """
        route = Route(self.start)
        visited = [self.start]
        stack = []
        while self.current_position != self.end:

            self.convergence_iter -= 1

            if self.convergence_iter == 0:
                return None

            surrounding_pheromone = self.maze.get_surrounding_pheromone(self.current_position)
            tot_pheromones = surrounding_pheromone.get_total_surrounding_pheromone()

            # Cumulative probabilities
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
