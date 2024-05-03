import math
import random
import numpy as np

from agents.Agent import Agent
from environments.Environment import Environment
from helpers.Coordinate import Coordinate
from helpers.PathSpecification import PathSpecification
from helpers.Route import Route


class Firefly(Agent):
    """
    Firefly is a class that represents a firefly in the Firefly Algorithm.
    """

    def __init__(self, environment: Environment, path_specification: PathSpecification, alpha_init, alpha_end, beta,
                 gamma_init, gamma_end, step_size: int = 1, obstacle_distance: int = 0):
        super().__init__(environment, path_specification, step_size)

        self.alpha_init = alpha_init
        self.alpha_end = alpha_end
        self.beta = beta
        self.gamma_init = gamma_init
        self.gamma_end = gamma_end
        self.__intensity: float = 0.0
        self.obstacle_distance = obstacle_distance
        self.route = Route(path_specification.start)

        self.current_position: Coordinate = path_specification.start
        self.update_intensity()

    @property
    def intensity(self):
        return self.__intensity

    @property
    def position(self):
        return self.current_position

    @position.setter
    def position(self, value: Coordinate):
        self.current_position = value

    def move_towards(self, better_position: Coordinate, adaptive) -> Coordinate:
        # Adaptive parameters
        alpha = self.alpha_init + adaptive * (self.alpha_end - self.alpha_init)
        gamma = self.gamma_init + adaptive * (self.gamma_end - self.gamma_init)

        # We compute the Euclidean distance between the particles
        distance = self.current_position.distance_to(better_position)
        attractiveness = self.beta * np.exp(-gamma * (distance ** 2))
        # The following can be changed with another distribution
        # random_number = random.uniform(0, 1) - 0.5
        random_number = self.levy_flight(beta=1.5, size=2)

        new_pos_x = self.current_position.x + (attractiveness * (better_position.x - self.current_position.x) +
                                               alpha * random_number[0])
        new_pos_y = self.current_position.y + (attractiveness * (better_position.y - self.current_position.y) +
                                               alpha * random_number[1])
        # Try also (from http://dx.doi.org/10.1155/2015/561394):
        # new_pos_x = self.current_position.x + (attractiveness * (better_position.x - self.current_position.x) +
        #                                        alpha * distance * random_number[0])
        # new_pos_y = self.current_position.y + (attractiveness * (better_position.y - self.current_position.y) +
        #                                        alpha * distance * random_number[1])

        if not self.position_out_of_bounds(Coordinate(new_pos_x, new_pos_y), obstacle_distance=self.obstacle_distance):
            self.current_position = Coordinate(new_pos_x, new_pos_y)
            self.route.add(self.current_position)

        return self.current_position  # return the current position

    def random_move(self):
        # levy_steps = self.levy_flight(beta=1.5, size=2)
        # levy_vel_x: float = levy_steps[0]
        # levy_vel_y: float = levy_steps[1]
        # levy_pos = Coordinate(self.current_position.x + levy_vel_x,
        #                       self.current_position.y + levy_vel_y)
        #
        # # Take the direction that is allowed
        # if self.environment.distance_to_closest_obstacle(levy_pos) > 0:
        #     if 0 <= levy_pos.x <= self.environment.width - 1:
        #         self.current_position.x = levy_pos.x
        #     if 0 <= levy_pos.y <= self.environment.height - 1:
        #         self.current_position.y = levy_pos.y
        #     self.route.add(self.current_position)
        area = 0.1
        self.current_position = Coordinate(
            random.uniform(self.current_position.x - area, self.current_position.x + area),
            random.uniform(self.current_position.y - area, self.current_position.y + area))

    def levy_flight(self, beta: float, size: int):
        # Draw samples from a uniform distribution
        u = np.random.uniform(0.01, 1, size=size)

        # Calculate the corresponding step lengths
        steps = u ** (-1 / beta)

        # Make sure the steps are between -2 and 2 (obstacle radius)
        steps = np.clip(steps, -2, 2)

        return steps

    def reach_end(self):
        """
        Check if the firefly has reached the end of the path.
        :return: True if the firefly has reached the end, False otherwise.
        """

        if self.route.get_route()[-1].x_between(self.environment.end.x - 0.5,
                                                self.environment.end.x + 0.5) and \
                self.route.get_route()[-1].y_between(self.environment.end.y - 0.5,
                                                     self.environment.end.y + 0.5):
            self.route.add(self.environment.end)
            return True
        return False

    def update_intensity(self) -> None:
        """
        Update the intensity of the firefly.
        """

        # We want to maximize the brightness, and minimize the objective function (distance to the goal)
        # Hence, we negate the objective function to get the intensity
        self.__intensity = -1 * self.objective_function()

    def objective_function(self) -> float:
        distance_to_goal = math.sqrt((self.current_position.x - self.environment.end.x) ** 2 + (
                self.current_position.y - self.environment.end.y) ** 2)
        # For now, we assign weight 1 to the goal distance and 0 to the obstacle distance
        # effectively only the goal distance is considered
        weight_goal: float = 1.0
        # The fireflies go to the 'brighter' firefly, i.e. the one with the lowest distance and the largest distance to
        # obstacles.

        return weight_goal * distance_to_goal
