import random
import numpy as np

from helpers.Coordinate import Coordinate


class Firefly:
    """
    Firefly is a class that represents a firefly in the Firefly Algorithm.
    """

    def __init__(self, alpha_init, alpha_end, beta, gamma_init, gamma_end, upper_boundary, lower_boundary):
        self.alpha_init = alpha_init
        self.alpha_end = alpha_end
        self.beta = beta
        self.gamma_init = gamma_init
        self.gamma_end = gamma_end
        self.__intensity = None
        self.lower_boundary = lower_boundary
        self.upper_boundary = upper_boundary
        self.current_position: Coordinate = Coordinate(random.uniform(lower_boundary, upper_boundary),
                                           random.uniform(lower_boundary, upper_boundary))

    @property
    def intensity(self):
        return self.__intensity

    @property
    def position(self):
        return self.current_position

    @position.setter
    def position(self, value: Coordinate):
        self.current_position = value

    def move_towards(self, better_position: Coordinate, adaptive):
        # Adaptive parameters
        alpha = self.alpha_init + adaptive * (self.alpha_end - self.alpha_init)
        gamma = self.gamma_init + adaptive * (self.gamma_end - self.gamma_init)

        # We compute the Euclidean distance between the particles
        distance = self.current_position.distance_to(better_position)
        attractiveness = self.beta * np.exp(-gamma * (distance ** 2))
        # The following can be changed with another distribution
        random_number = random.uniform(0, 1) - 0.5

        self.current_position.x += (attractiveness * (better_position.x - self.current_position.x) +
                                    alpha * random_number)
        self.current_position.y += (attractiveness * (better_position.y - self.current_position.y) +
                                    alpha * random_number)
        # Try also (from http://dx.doi.org/10.1155/2015/561394):
        # self.__position += (attractiveness * (better_position - self.__position) +
        #                     alpha * distance * random_number)
        self.check_boundaries()

    def update_intensity(self, func) -> None:
        """
        Update the intensity of the firefly.
        """
        self.__intensity = -1 * func(self.current_position)

    def check_boundaries(self) -> None:
        """
        Check if the current position is within the boundaries of the search space. If not, set it to the closest.
        """

        self.current_position.x = min(max(self.lower_boundary, self.current_position.x), self.upper_boundary)
        self.current_position.y = min(max(self.lower_boundary, self.current_position.y), self.upper_boundary)
